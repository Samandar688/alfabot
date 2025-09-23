
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALFABOT — Consolidated Database Setup (Merged Schema)
----------------------------------------------------
• Merged from 3 analysis reports (2025-09-22)
• Safe on Windows/Linux (UTF-8, no LC_* forcing)
• Idempotent: re-runnable (IF NOT EXISTS / DO $$ ... $$)
• Legacy-compat layer: connections.connecion_id <-> connection_order_id sync
• Rich bilingual (UZ/RU) seed data

How to run:
  1) (optional) set env: PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
  2) python3 alfa_setup_merged.py
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'port': int(os.getenv('PGPORT', '5432')),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', 'ulugbek202'),
    'database': os.getenv('PGDATABASE', 'alfa_db_merged'),
}

def create_database():
    """Create DB (UTF8) if missing. Avoid Windows locale issues."""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_CONFIG['database']} WITH TEMPLATE template0 ENCODING 'UTF8'")
            print(f"[+] Database '{DB_CONFIG['database']}' created (UTF-8)")
        else:
            print(f"[=] Database '{DB_CONFIG['database']}' already exists")
        cur.close(); conn.close()
        return True
    except Exception as e:
        print(f"[!] create_database error: {e}")
        return False

SCHEMA_SQL = r"""
-- ===============================================
-- ALFABOT MERGED SCHEMA  (generated 2025-09-22T11:43:54.965373Z)
-- ===============================================
SET client_encoding = 'UTF8';

-- ===== ENUM TYPES =====
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='user_role' AND n.nspname='public') THEN
    CREATE TYPE public.user_role AS ENUM
      ('admin','client','manager','junior_manager','controller','technician','warehouse',
       'callcenter_supervisor','callcenter_operator');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='connection_order_status' AND n.nspname='public') THEN
    CREATE TYPE public.connection_order_status AS ENUM
      ('new','in_manager','in_junior_manager','in_controller','in_technician','in_diagnostics',
       'in_repairs','in_warehouse','in_technician_work','completed','in_call_center',
       'in_call_center_operator','in_call_center_supervisor');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='technician_order_status' AND n.nspname='public') THEN
    CREATE TYPE public.technician_order_status AS ENUM
      ('new','in_controller','in_technician','in_diagnostics','in_repairs','in_warehouse',
       'in_technician_work','completed','cancelled');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='saff_order_status' AND n.nspname='public') THEN
    CREATE TYPE public.saff_order_status AS ENUM
      ('in_call_center','in_manager','in_controller','in_technician','completed','cancelled');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='type_of_zayavka' AND n.nspname='public') THEN
    CREATE TYPE public.type_of_zayavka AS ENUM ('connection','technician');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='smart_service_category' AND n.nspname='public') THEN
    CREATE TYPE public.smart_service_category AS ENUM ('internet','tv','phone','other');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
                 WHERE t.typname='smart_service_type' AND n.nspname='public') THEN
    CREATE TYPE public.smart_service_type AS ENUM ('internet','tv','phone','other');
  END IF;
END $$;

-- ===== COMMON FUNCTIONS (updated_at) =====
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ===== USERS =====
CREATE TABLE IF NOT EXISTS public.users (
  id           BIGSERIAL PRIMARY KEY,
  telegram_id  BIGINT UNIQUE,
  full_name    TEXT,
  username     TEXT,
  phone        TEXT,
  language     VARCHAR(5) NOT NULL DEFAULT 'uz',
  region       INTEGER,
  address      TEXT,
  role         public.user_role,
  abonent_id   TEXT,
  is_blocked   BOOLEAN NOT NULL DEFAULT FALSE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_abonent_id ON public.users(abonent_id);
CREATE INDEX IF NOT EXISTS idx_users_role       ON public.users(role);
DROP TRIGGER IF EXISTS trg_users_updated_at ON public.users;
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== TARIF =====
CREATE TABLE IF NOT EXISTS public.tarif (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT,
  picture    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
DROP TRIGGER IF EXISTS trg_tarif_updated_at ON public.tarif;
CREATE TRIGGER trg_tarif_updated_at BEFORE UPDATE ON public.tarif
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== CONNECTION_ORDERS =====
CREATE TABLE IF NOT EXISTS public.connection_orders (
  id               BIGSERIAL PRIMARY KEY,
  user_id          BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  region           TEXT,
  address          TEXT,
  tarif_id         BIGINT REFERENCES public.tarif(id) ON DELETE SET NULL,
  longitude        DOUBLE PRECISION,
  latitude         DOUBLE PRECISION,
  rating           INTEGER,
  notes            TEXT,
  jm_notes         TEXT,
  controller_notes TEXT NOT NULL DEFAULT '',
  is_active        BOOLEAN NOT NULL DEFAULT TRUE,
  status           public.connection_order_status NOT NULL DEFAULT 'new',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_connection_orders_user    ON public.connection_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_connection_orders_status  ON public.connection_orders(status);
CREATE INDEX IF NOT EXISTS idx_connection_orders_created ON public.connection_orders(created_at);
DROP TRIGGER IF EXISTS trg_connection_orders_updated_at ON public.connection_orders;
CREATE TRIGGER trg_connection_orders_updated_at BEFORE UPDATE ON public.connection_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== TECHNICIAN_ORDERS =====
CREATE TABLE IF NOT EXISTS public.technician_orders (
  id                   BIGSERIAL PRIMARY KEY,
  user_id              BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  region               INTEGER,
  abonent_id           TEXT,
  address              TEXT,
  media                TEXT,
  longitude            DOUBLE PRECISION,
  latitude             DOUBLE PRECISION,
  description          TEXT,
  description_ish      TEXT,
  description_operator TEXT,
  status               public.technician_order_status NOT NULL DEFAULT 'new',
  rating               INTEGER,
  notes                TEXT,
  is_active            BOOLEAN NOT NULL DEFAULT TRUE,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_technician_orders_user    ON public.technician_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_technician_orders_status  ON public.technician_orders(status);
CREATE INDEX IF NOT EXISTS idx_technician_orders_created ON public.technician_orders(created_at);
DROP TRIGGER IF EXISTS trg_technician_orders_updated_at ON public.technician_orders;
CREATE TRIGGER trg_technician_orders_updated_at BEFORE UPDATE ON public.technician_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== SAFF_ORDERS =====
CREATE TABLE IF NOT EXISTS public.saff_orders (
  id             BIGSERIAL PRIMARY KEY,
  user_id        BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  phone          TEXT,
  region         INTEGER,
  abonent_id     TEXT,
  tarif_id       BIGINT REFERENCES public.tarif(id) ON DELETE SET NULL,
  address        TEXT,
  description    TEXT,
  status         public.saff_order_status NOT NULL DEFAULT 'in_call_center',
  type_of_zayavka public.type_of_zayavka NOT NULL DEFAULT 'connection',
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_saff_orders_user   ON public.saff_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_saff_orders_status ON public.saff_orders(status);
CREATE INDEX IF NOT EXISTS idx_saff_status_active ON public.saff_orders(status, is_active);
CREATE INDEX IF NOT EXISTS idx_saff_ccs_active_created
  ON public.saff_orders(created_at, id)
  WHERE (status = 'in_call_center'::public.saff_order_status AND is_active = TRUE);
DROP TRIGGER IF EXISTS trg_saff_orders_updated_at ON public.saff_orders;
CREATE TRIGGER trg_saff_orders_updated_at BEFORE UPDATE ON public.saff_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== SMART_SERVICE_ORDERS =====
CREATE TABLE IF NOT EXISTS public.smart_service_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  category     public.smart_service_category NOT NULL,
  service_type public.smart_service_type NOT NULL,
  address      TEXT NOT NULL,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_sso_user_id       ON public.smart_service_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_sso_category      ON public.smart_service_orders(category);
CREATE INDEX IF NOT EXISTS idx_sso_created       ON public.smart_service_orders(created_at);
CREATE INDEX IF NOT EXISTS idx_sso_created_desc  ON public.smart_service_orders(created_at DESC);
DROP TRIGGER IF EXISTS trg_sso_updated_at ON public.smart_service_orders;
CREATE TRIGGER trg_sso_updated_at BEFORE UPDATE ON public.smart_service_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== MATERIALS =====
CREATE TABLE IF NOT EXISTS public.materials (
  id            SERIAL PRIMARY KEY,
  name          VARCHAR(255),
  price         NUMERIC,
  description   TEXT,
  quantity      INTEGER DEFAULT 0,
  serial_number VARCHAR(100) UNIQUE,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_materials_name   ON public.materials(name);
CREATE INDEX IF NOT EXISTS idx_materials_serial ON public.materials(serial_number);
DROP TRIGGER IF EXISTS trg_materials_updated_at ON public.materials;
CREATE TRIGGER trg_materials_updated_at BEFORE UPDATE ON public.materials
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== MATERIAL_AND_TECHNICIAN =====
CREATE TABLE IF NOT EXISTS public.material_and_technician (
  id          SERIAL PRIMARY KEY,
  user_id     INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  material_id INTEGER NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
  quantity    INTEGER
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_mat_tech_user_material
  ON public.material_and_technician(user_id, material_id);

-- ===== MATERIAL_REQUESTS =====
CREATE TABLE IF NOT EXISTS public.material_requests (
  id                   SERIAL PRIMARY KEY,
  description          TEXT,
  user_id              INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  applications_id      INTEGER NOT NULL,
  material_id          INTEGER NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
  connection_order_id  INTEGER REFERENCES public.connection_orders(id) ON DELETE SET NULL,
  technician_order_id  INTEGER REFERENCES public.technician_orders(id) ON DELETE SET NULL,
  saff_order_id        INTEGER REFERENCES public.saff_orders(id) ON DELETE SET NULL,
  quantity             INTEGER DEFAULT 1,
  price                NUMERIC DEFAULT 0,
  total_price          NUMERIC DEFAULT 0
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_material_requests_triplet
  ON public.material_requests(user_id, applications_id, material_id);
CREATE INDEX IF NOT EXISTS idx_material_requests_user ON public.material_requests(user_id);

-- ===== REPORTS (normalized to users.id) =====
CREATE TABLE IF NOT EXISTS public.reports (
  id          SERIAL PRIMARY KEY,
  title       TEXT NOT NULL,
  description TEXT,
  created_by  BIGINT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- Drop existing FKs then recreate canonical
DO $$ BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.table_constraints
    WHERE table_schema='public' AND table_name='reports' AND constraint_type='FOREIGN KEY'
  ) THEN
    EXECUTE (
      SELECT 'ALTER TABLE public.reports DROP CONSTRAINT ' || quote_ident(tc.constraint_name)
      FROM information_schema.table_constraints tc
      WHERE tc.table_schema='public' AND tc.table_name='reports' AND tc.constraint_type='FOREIGN KEY'
      LIMIT 1
    );
  END IF;
EXCEPTION WHEN undefined_object THEN
  NULL;
END $$;
ALTER TABLE public.reports
  ADD CONSTRAINT fk_reports_created_by_user
  FOREIGN KEY (created_by) REFERENCES public.users(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS idx_reports_created_by ON public.reports(created_by);
DROP TRIGGER IF EXISTS trg_reports_updated_at ON public.reports;
CREATE TRIGGER trg_reports_updated_at BEFORE UPDATE ON public.reports
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== AKT_DOCUMENTS / AKT_RATINGS =====
CREATE TABLE IF NOT EXISTS public.akt_documents (
  id               SERIAL PRIMARY KEY,
  request_id       INTEGER NOT NULL,
  request_type     VARCHAR(20) NOT NULL,
  akt_number       VARCHAR(50) NOT NULL,
  file_path        VARCHAR(255) NOT NULL,
  file_hash        VARCHAR(64) NOT NULL,
  created_at       TIMESTAMPTZ DEFAULT NOW(),
  sent_to_client_at TIMESTAMPTZ
);
CREATE UNIQUE INDEX IF NOT EXISTS akt_documents_request_id_request_type_key
  ON public.akt_documents(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_documents_request ON public.akt_documents(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_documents_created ON public.akt_documents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_akt_documents_sent    ON public.akt_documents(sent_to_client_at);

CREATE TABLE IF NOT EXISTS public.akt_ratings (
  id           SERIAL PRIMARY KEY,
  request_id   INTEGER NOT NULL,
  request_type VARCHAR(20) NOT NULL,
  rating       INTEGER NOT NULL,
  comment      TEXT,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS akt_ratings_request_id_request_type_key
  ON public.akt_ratings(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_ratings_request ON public.akt_ratings(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_ratings_rating  ON public.akt_ratings(rating);
CREATE INDEX IF NOT EXISTS idx_akt_ratings_created ON public.akt_ratings(created_at DESC);

-- ===== CONNECTIONS (with legacy sync) =====
CREATE TABLE IF NOT EXISTS public.connections (
  id                  BIGSERIAL PRIMARY KEY,
  sender_id           BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  recipient_id        BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  connection_order_id BIGINT REFERENCES public.connection_orders(id) ON DELETE SET NULL,
  technician_id       BIGINT REFERENCES public.technician_orders(id) ON DELETE SET NULL,
  saff_id             BIGINT REFERENCES public.saff_orders(id) ON DELETE SET NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sender_status       TEXT,
  recipient_status    TEXT
);
-- Legacy column to keep old queries working
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='public' AND table_name='connections' AND column_name='connecion_id'
  ) THEN
    ALTER TABLE public.connections ADD COLUMN connecion_id INTEGER;
    UPDATE public.connections SET connecion_id = connection_order_id::int
    WHERE connection_order_id IS NOT NULL AND connecion_id IS NULL;
  END IF;
END $$;

CREATE OR REPLACE FUNCTION public.trg_sync_connections_ids()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.connection_order_id IS NULL AND NEW.connecion_id IS NOT NULL THEN
    NEW.connection_order_id := NEW.connecion_id::bigint;
  ELSIF NEW.connecion_id IS NULL AND NEW.connection_order_id IS NOT NULL THEN
    NEW.connecion_id := NEW.connection_order_id::int;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sync_connections_ids_bi ON public.connections;
CREATE TRIGGER trg_sync_connections_ids_bi BEFORE INSERT OR UPDATE ON public.connections
FOR EACH ROW EXECUTE FUNCTION public.trg_sync_connections_ids();

CREATE INDEX IF NOT EXISTS idx_connections_sender_id     ON public.connections(sender_id);
CREATE INDEX IF NOT EXISTS idx_connections_recipient_id  ON public.connections(recipient_id);
CREATE INDEX IF NOT EXISTS idx_connections_technician_id ON public.connections(technician_id);
DROP TRIGGER IF EXISTS trg_connections_updated_at ON public.connections;
CREATE TRIGGER trg_connections_updated_at BEFORE UPDATE ON public.connections
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===============================================
-- BILINGUAL SEED DATA (UZ / RU)
-- ===============================================

-- Tariffs (UZ/RU mix)
INSERT INTO public.tarif (name, picture) VALUES
  ('Hammasi birga 4', ''),
  ('Hammasi birga 3+', ''),
  ('Hammasi birga 3', ''),
  ('Hammasi birga 2', ''),
  ('Домашний Интернет+', ''),
  ('Супер ТВ пакет', '')
ON CONFLICT DO NOTHING;

-- Users (roles wide, bilingually named)
INSERT INTO public.users (telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked) VALUES
  (1978574076, 'Ulug‘bek Administrator', 'ulugbekbb', '998900042544', 'uz', 1, 'Toshkent shahri', 'admin', 'ADM001', FALSE),
  (210000001, 'Aziz Karimov', 'aziz_k', '998901234567', 'uz', 1, 'Chilonzor tumani', 'client', '1001', FALSE),
  (210000002, 'Nodira Toshmatova', 'nodira_t', '998912345678', 'uz', 2, 'Registon ko‘chasi', 'manager', 'MGR001', FALSE),
  (210000003, 'Bobur Alimov', 'bobur_a', '998923456789', 'uz', 3, 'Alpomish mahallasi', 'technician', 'TECH001', FALSE),
  (210000004, 'Malika Rahimova', 'malika_r', '998934567890', 'uz', 4, 'Yuksalish ko‘chasi', 'controller', 'CTRL001', FALSE),
  (210000005, 'Jasur Nazarov', 'jasur_n', '998945678901', 'uz', 5, 'Mirzo Ulug‘bek tumani', 'junior_manager', 'JM001', FALSE),
  (210000006, 'Dilnoza Yusupova', 'dilnoza_y', '998956789012', 'uz', 1, 'Yakkasaroy tumani', 'warehouse', 'WH001', FALSE),
  (310000001, 'Александр Петров', 'alex_petrov', '998911223344', 'ru', 1, 'ул. Пушкина, 15', 'client', '2001', FALSE),
  (310000002, 'Елена Смирнова', 'elena_smirnova', '998922334455', 'ru', 2, 'пр. Ленина, 42', 'manager', 'MGR003', FALSE),
  (310000003, 'Дмитрий Козлов', 'dmitry_kozlov', '998933445566', 'ru', 3, 'ул. Гагарина, 28', 'technician', 'TECH004', FALSE),
  (310000004, 'Ольга Васильева', 'olga_vasileva', '998944556677', 'ru', 4, 'ул. Советская, 67', 'controller', 'CTRL003', FALSE),
  (310000005, 'Сергей Николаев', 'sergey_nikolaev', '998955667788', 'ru', 5, 'пр. Мира, 89', 'junior_manager', 'JM002', FALSE),
  (310000006, 'Татьяна Морозова', 'tatyana_morozova', '998988990011', 'ru', 3, 'пр. Победы, 78', 'callcenter_operator', 'CCO002', FALSE)
ON CONFLICT DO NOTHING;

-- Materials (mixed)
INSERT INTO public.materials (name, price, description, quantity, serial_number) VALUES
  ('Optik kabel', 15000, 'Tashqi muhit uchun optik tolali kabel, 1km', 500, 'OPT-001'),
  ('Router TP-Link', 450000, 'Wi‑Fi router, 4 port, 300Mbps', 25, 'RTR-001'),
  ('Splitter 1x8', 35000, 'Optik splitter, 1 kirish 8 chiqish', 100, 'SPL-001'),
  ('ONT Huawei', 320000, 'Optical Network Terminal, GPON', 50, 'ONT-001'),
  ('Patch cord', 8000, 'SC/UPC-SC/UPC, 3m', 200, 'PC-001'),
  ('Кабель оптический', 18000, 'Оптоволоконный кабель, 1км', 300, 'OPT-002'),
  ('Роутер D-Link', 380000, 'Wi‑Fi роутер, 4 порта, 300Mbps', 30, 'RTR-002'),
  ('Сплиттер 1x16', 65000, 'Оптический сплиттер, 1x16', 75, 'SPL-002'),
  ('ONT ZTE', 290000, 'GPON ONT', 40, 'ONT-002'),
  ('Патч-корд', 9500, 'SC/UPC-SC/UPC, 5м', 150, 'PC-002'),
  ('Kabel UTP Cat6', 2500, 'UTP 1m', 1000, 'UTP-001'),
  ('Connector RJ45', 500, 'RJ45 ulagich', 500, 'RJ45-001'),
  ('Switch 8 port', 180000, 'Gigabit 8-port', 20, 'SW-001'),
  ('Кабель UTP Cat6', 2800, 'UTP 1м', 800, 'UTP-002'),
  ('Коннектор RJ45', 600, 'RJ45 разъем', 400, 'RJ45-002')
ON CONFLICT DO NOTHING;

-- Connection orders (UZ/RU)
INSERT INTO public.connection_orders (user_id, region, address, tarif_id, longitude, latitude, status, notes, jm_notes)
SELECT u.id, 'Toshkent', 'Chilonzor tumani, 12-45', 1, 69.240562, 41.311158, 'new', 'Yangi ulanish arizasi', ''
FROM public.users u WHERE u.username='aziz_k'
ON CONFLICT DO NOTHING;

INSERT INTO public.connection_orders (user_id, region, address, tarif_id, longitude, latitude, status, notes, jm_notes)
SELECT u.id, 'Toshkent', 'Yunusobod tumani, 8-23', 2, 69.289398, 41.327142, 'in_manager', 'Manager tekshirmoqda', 'Hujjatlar to‘liq'
FROM public.users u WHERE u.username='ulugbekbb'
ON CONFLICT DO NOTHING;

INSERT INTO public.connection_orders (user_id, region, address, tarif_id, longitude, latitude, status, notes, jm_notes)
SELECT u.id, 'г. Ташкент', 'ул. Пушкина, 25-12', 4, 69.240562, 41.311158, 'in_controller', 'На проверке контроллера', 'Документы в порядке'
FROM public.users u WHERE u.username='alex_petrov'
ON CONFLICT DO NOTHING;

-- Technician orders
INSERT INTO public.technician_orders (user_id, region, abonent_id, address, description, status)
SELECT u.id, 1, '1001', 'Chilonzor, 1-mavze', 'Internet uzilib turadi', 'new'
FROM public.users u WHERE u.username='aziz_k'
ON CONFLICT DO NOTHING;

INSERT INTO public.technician_orders (user_id, region, abonent_id, address, description, status)
SELECT u.id, 3, 'TECH004', 'ул. Гагарина, 28', 'Проблемы с подключением', 'completed'
FROM public.users u WHERE u.username='dmitry_kozlov'
ON CONFLICT DO NOTHING;

-- Saff orders
INSERT INTO public.saff_orders (user_id, phone, abonent_id, address, tarif_id, description, status)
SELECT u.id, '998901112233', '1010', 'Yunusobod 5-uy', 2, 'Xizmat sifatini tekshirish', 'in_manager'
FROM public.users u WHERE u.username='ulugbekbb'
ON CONFLICT DO NOTHING;

INSERT INTO public.saff_orders (user_id, phone, abonent_id, address, tarif_id, description, status)
SELECT u.id, '998911223344', '2001', 'ул. Пушкина, 15', 1, 'Проверка качества услуг', 'in_controller'
FROM public.users u WHERE u.username='alex_petrov'
ON CONFLICT DO NOTHING;

-- Smart service orders
INSERT INTO public.smart_service_orders (user_id, category, service_type, address, longitude, latitude, is_active)
SELECT u.id, 'internet','internet','Chilonzor, 1-mavze',69.240562,41.311158,TRUE
FROM public.users u WHERE u.username='aziz_k'
ON CONFLICT DO NOTHING;

INSERT INTO public.smart_service_orders (user_id, category, service_type, address, is_active)
SELECT u.id, 'tv','tv','Yunusobod 5-uy',TRUE
FROM public.users u WHERE u.username='ulugbekbb'
ON CONFLICT DO NOTHING;

-- Connections (with legacy column sync)
INSERT INTO public.connections (sender_id, recipient_id, connection_order_id, technician_id, saff_id, sender_status, recipient_status)
SELECT u1.id, u2.id, co.id, NULL, NULL, 'in_call_center_operator','in_controller'
FROM public.users u1, public.users u2, public.connection_orders co
WHERE u1.username='alex_petrov' AND u2.username='ulugbekbb'
ON CONFLICT DO NOTHING;

-- Material requests (with triplet unique)
INSERT INTO public.material_requests (description, user_id, applications_id, material_id, connection_order_id, quantity, price, total_price)
SELECT 'Optik kabel kerak', u.id, 1, m.id, co.id, 100, 15000, 1500000
FROM public.users u, public.materials m, public.connection_orders co
WHERE u.username='bobur_a' AND m.serial_number='OPT-001'
ON CONFLICT DO NOTHING;

-- Reports (normalized to users.id)
INSERT INTO public.reports (title, description, created_by)
SELECT 'Ulanish bo‘yicha hisobot', 'Yangi ulanish yakunlandi', u.id
FROM public.users u WHERE u.username='bobur_a'
ON CONFLICT DO NOTHING;

-- AKT docs/ratings
INSERT INTO public.akt_documents (request_id, request_type, akt_number, file_path, file_hash)
VALUES (1,'connection','AKT-001','/documents/akt_001.pdf','hash001')
ON CONFLICT DO NOTHING;

INSERT INTO public.akt_ratings (request_id, request_type, rating, comment)
VALUES (1,'connection',5,'Juda yaxshi xizmat')
ON CONFLICT DO NOTHING;
"""

def run_sql(conn, sql_text):
    cur = conn.cursor()
    # split by semicolon but keep DO $$ ... $$ blocks intact by naive approach:
    # We'll execute as one big block to preserve DO $$ blocks and triggers reliably.
    cur.execute(sql_text)
    cur.close()

def verify_setup():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()

        print("\n[✓] Verifying...")
        cur.execute("""SELECT COUNT(*) FROM information_schema.tables
                        WHERE table_schema='public' AND table_type='BASE TABLE'""")
        print("Tables:", cur.fetchone()[0])

        for tbl in ['users','tarif','connection_orders','technician_orders','saff_orders',
                    'smart_service_orders','materials','material_and_technician',
                    'material_requests','reports','akt_documents','akt_ratings','connections']:
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            cnt = cur.fetchone()[0]
            print(f"  - {tbl}: {cnt} rows" if cnt else f"  - {tbl}: empty")


        # quick enum presence
        cur.execute("SELECT typname FROM pg_type WHERE typtype='e' AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname='public') ORDER BY 1")
        enums = [r[0] for r in cur.fetchall()]
        print("Enums:", ', '.join(enums))

        cur.close(); conn.close()
        return True
    except Exception as e:
        print(f"[!] verify_setup error: {e}")
        return False

def main():
    print("🚀 ALFABOT merged setup start")
    if not create_database():
        sys.exit(1)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        print("[>] Applying schema & seeds...")
        run_sql(conn, SCHEMA_SQL)
        conn.commit()
        conn.close()
        print("✅ Done.")
    except Exception as e:
        print(f"[!] setup error: {e}")
        sys.exit(1)

    ok = verify_setup()
    print("🎉 Ready" if ok else "⚠️ Verify had issues")


if __name__ == '__main__':
    main()
