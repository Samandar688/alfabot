#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALFABOT — Clean Database Setup
------------------------------
• Creates complete database schema with all tables, enums, foreign keys, and indexes
• Only inserts one admin user, no other seed data
• Safe on Windows/Linux (UTF-8, no LC_* forcing)
• Idempotent: re-runnable (IF NOT EXISTS / DO $$ ... $$)

How to run:
  1) (optional) set env: PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
  2) python3 setup.py
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
    'database': os.getenv('PGDATABASE', 'alfa_db_clean'),
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
-- ALFABOT CLEAN SCHEMA (Only Admin User)
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

-- ===== HELPER FUNCTIONS =====
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ===== MAIN TABLES =====

-- USERS
CREATE TABLE IF NOT EXISTS public.users (
  id           BIGSERIAL PRIMARY KEY,
  telegram_id  BIGINT UNIQUE,
  full_name    TEXT NOT NULL,
  username     TEXT UNIQUE,
  phone        TEXT,
  language     TEXT DEFAULT 'uz',
  region       INTEGER,
  address      TEXT,
  role         public.user_role NOT NULL DEFAULT 'client',
  abonent_id   TEXT UNIQUE,
  is_blocked   BOOLEAN NOT NULL DEFAULT FALSE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON public.users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_role ON public.users(role);
CREATE INDEX IF NOT EXISTS idx_users_abonent_id ON public.users(abonent_id);
DROP TRIGGER IF EXISTS trg_users_updated_at ON public.users;
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- TARIF
CREATE TABLE IF NOT EXISTS public.tarif (
  id          BIGSERIAL PRIMARY KEY,
  name        TEXT NOT NULL,
  price       BIGINT NOT NULL,
  description TEXT,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_tarif_is_active ON public.tarif(is_active);
DROP TRIGGER IF EXISTS trg_tarif_updated_at ON public.tarif;
CREATE TRIGGER trg_tarif_updated_at BEFORE UPDATE ON public.tarif
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- CONNECTION_ORDERS
CREATE TABLE IF NOT EXISTS public.connection_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  region       TEXT,
  address      TEXT NOT NULL,
  tarif_id     BIGINT REFERENCES public.tarif(id) ON DELETE SET NULL,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  status       public.connection_order_status NOT NULL DEFAULT 'new',
  notes        TEXT,
  jm_notes     TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_connection_orders_user ON public.connection_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_connection_orders_status ON public.connection_orders(status);
CREATE INDEX IF NOT EXISTS idx_connection_orders_tarif ON public.connection_orders(tarif_id);
CREATE INDEX IF NOT EXISTS idx_connection_status_active ON public.connection_orders(status, is_active);
DROP TRIGGER IF EXISTS trg_connection_orders_updated_at ON public.connection_orders;
CREATE TRIGGER trg_connection_orders_updated_at BEFORE UPDATE ON public.connection_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- TECHNICIAN_ORDERS
CREATE TABLE IF NOT EXISTS public.technician_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  region       TEXT,
  address      TEXT NOT NULL,
  tarif_id     BIGINT REFERENCES public.tarif(id) ON DELETE SET NULL,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  status       public.technician_order_status NOT NULL DEFAULT 'new',
  notes        TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_technician_orders_user ON public.technician_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_technician_orders_status ON public.technician_orders(status);
CREATE INDEX IF NOT EXISTS idx_technician_orders_tarif ON public.technician_orders(tarif_id);
CREATE INDEX IF NOT EXISTS idx_tech_status_active ON public.technician_orders(status, is_active);
DROP TRIGGER IF EXISTS trg_technician_orders_updated_at ON public.technician_orders;
CREATE TRIGGER trg_technician_orders_updated_at BEFORE UPDATE ON public.technician_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- SAFF_ORDERS
CREATE TABLE IF NOT EXISTS public.saff_orders (
  id             BIGSERIAL PRIMARY KEY,
  user_id        BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  phone          TEXT,
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
CREATE INDEX IF NOT EXISTS idx_saff_orders_user ON public.saff_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_saff_orders_status ON public.saff_orders(status);
CREATE INDEX IF NOT EXISTS idx_saff_status_active ON public.saff_orders(status, is_active);
CREATE INDEX IF NOT EXISTS idx_saff_ccs_active_created
  ON public.saff_orders(created_at, id)
  WHERE (status = 'in_call_center'::public.saff_order_status AND is_active = TRUE);
DROP TRIGGER IF EXISTS trg_saff_orders_updated_at ON public.saff_orders;
CREATE TRIGGER trg_saff_orders_updated_at BEFORE UPDATE ON public.saff_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- SMART_SERVICE_ORDERS
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
CREATE INDEX IF NOT EXISTS idx_smart_service_user ON public.smart_service_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_smart_service_category ON public.smart_service_orders(category);
CREATE INDEX IF NOT EXISTS idx_smart_service_type ON public.smart_service_orders(service_type);
DROP TRIGGER IF EXISTS trg_smart_service_orders_updated_at ON public.smart_service_orders;
CREATE TRIGGER trg_smart_service_orders_updated_at BEFORE UPDATE ON public.smart_service_orders
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- MATERIALS
CREATE TABLE IF NOT EXISTS public.materials (
  id            BIGSERIAL PRIMARY KEY,
  name          TEXT NOT NULL,
  price         BIGINT NOT NULL,
  description   TEXT,
  quantity      INTEGER NOT NULL DEFAULT 0,
  serial_number TEXT UNIQUE,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_materials_serial ON public.materials(serial_number);
CREATE INDEX IF NOT EXISTS idx_materials_is_active ON public.materials(is_active);
DROP TRIGGER IF EXISTS trg_materials_updated_at ON public.materials;
CREATE TRIGGER trg_materials_updated_at BEFORE UPDATE ON public.materials
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- MATERIAL_AND_TECHNICIAN
CREATE TABLE IF NOT EXISTS public.material_and_technician (
  id           BIGSERIAL PRIMARY KEY,
  material_id  BIGINT NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
  technician_id BIGINT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  quantity     INTEGER NOT NULL DEFAULT 1,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(material_id, technician_id)
);
CREATE INDEX IF NOT EXISTS idx_mat_tech_material ON public.material_and_technician(material_id);
CREATE INDEX IF NOT EXISTS idx_mat_tech_technician ON public.material_and_technician(technician_id);
DROP TRIGGER IF EXISTS trg_material_and_technician_updated_at ON public.material_and_technician;
CREATE TRIGGER trg_material_and_technician_updated_at BEFORE UPDATE ON public.material_and_technician
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- MATERIAL_REQUESTS
CREATE TABLE IF NOT EXISTS public.material_requests (
  id                  BIGSERIAL PRIMARY KEY,
  description         TEXT,
  user_id             BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  applications_id     BIGINT,
  material_id         BIGINT REFERENCES public.materials(id) ON DELETE SET NULL,
  connection_order_id BIGINT REFERENCES public.connection_orders(id) ON DELETE SET NULL,
  quantity            INTEGER NOT NULL DEFAULT 1,
  price               BIGINT,
  total_price         BIGINT,
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, material_id, connection_order_id)
);
CREATE INDEX IF NOT EXISTS idx_material_requests_user ON public.material_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_material_requests_material ON public.material_requests(material_id);
CREATE INDEX IF NOT EXISTS idx_material_requests_connection ON public.material_requests(connection_order_id);
DROP TRIGGER IF EXISTS trg_material_requests_updated_at ON public.material_requests;
CREATE TRIGGER trg_material_requests_updated_at BEFORE UPDATE ON public.material_requests
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- REPORTS
CREATE TABLE IF NOT EXISTS public.reports (
  id          BIGSERIAL PRIMARY KEY,
  title       TEXT NOT NULL,
  description TEXT,
  created_by  BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reports_created_by ON public.reports(created_by);
CREATE INDEX IF NOT EXISTS idx_reports_is_active ON public.reports(is_active);
DROP TRIGGER IF EXISTS trg_reports_updated_at ON public.reports;
CREATE TRIGGER trg_reports_updated_at BEFORE UPDATE ON public.reports
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- AKT_DOCUMENTS
CREATE TABLE IF NOT EXISTS public.akt_documents (
  id           BIGSERIAL PRIMARY KEY,
  request_id   BIGINT NOT NULL,
  request_type TEXT NOT NULL,
  akt_number   TEXT UNIQUE NOT NULL,
  file_path    TEXT,
  file_hash    TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_akt_docs_request ON public.akt_documents(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_docs_number ON public.akt_documents(akt_number);
DROP TRIGGER IF EXISTS trg_akt_documents_updated_at ON public.akt_documents;
CREATE TRIGGER trg_akt_documents_updated_at BEFORE UPDATE ON public.akt_documents
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- AKT_RATINGS
CREATE TABLE IF NOT EXISTS public.akt_ratings (
  id           BIGSERIAL PRIMARY KEY,
  request_id   BIGINT NOT NULL,
  request_type TEXT NOT NULL,
  rating       INTEGER CHECK (rating >= 1 AND rating <= 5),
  comment      TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_akt_ratings_request ON public.akt_ratings(request_id, request_type);
CREATE INDEX IF NOT EXISTS idx_akt_ratings_rating ON public.akt_ratings(rating);
DROP TRIGGER IF EXISTS trg_akt_ratings_updated_at ON public.akt_ratings;
CREATE TRIGGER trg_akt_ratings_updated_at BEFORE UPDATE ON public.akt_ratings
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- CONNECTIONS (Legacy compatibility)
CREATE TABLE IF NOT EXISTS public.connections (
  id                 BIGSERIAL PRIMARY KEY,
  sender_id          BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  recipient_id       BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  connection_order_id BIGINT REFERENCES public.connection_orders(id) ON DELETE SET NULL,
  technician_id      BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
  saff_id            BIGINT REFERENCES public.saff_orders(id) ON DELETE SET NULL,
  sender_status      TEXT,
  recipient_status   TEXT,
  is_active          BOOLEAN NOT NULL DEFAULT TRUE,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_connections_sender ON public.connections(sender_id);
CREATE INDEX IF NOT EXISTS idx_connections_recipient ON public.connections(recipient_id);
CREATE INDEX IF NOT EXISTS idx_connections_order ON public.connections(connection_order_id);
DROP TRIGGER IF EXISTS trg_connections_updated_at ON public.connections;
CREATE TRIGGER trg_connections_updated_at BEFORE UPDATE ON public.connections
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ===== SEED DATA (ONLY ADMIN USER) =====
INSERT INTO public.users (telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked) VALUES
  (1978574076, 'Ulug''bek Administrator', 'ulugbekbb', '998900042544', 'uz', 1, 'Toshkent shahri', 'admin', 'ADM001', FALSE)
ON CONFLICT DO NOTHING;
"""

def run_sql(conn, sql_text):
    cur = conn.cursor()
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

        # Check admin user
        cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        admin_count = cur.fetchone()[0]
        print(f"Admin users: {admin_count}")

        # Check enums
        cur.execute("SELECT typname FROM pg_type WHERE typtype='e' AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname='public') ORDER BY 1")
        enums = [r[0] for r in cur.fetchall()]
        print("Enums:", ', '.join(enums))

        # Check indexes
        cur.execute("""SELECT COUNT(*) FROM pg_indexes WHERE schemaname='public'""")
        index_count = cur.fetchone()[0]
        print(f"Indexes: {index_count}")

        # Check foreign keys
        cur.execute("""SELECT COUNT(*) FROM information_schema.table_constraints 
                       WHERE constraint_schema='public' AND constraint_type='FOREIGN KEY'""")
        fk_count = cur.fetchone()[0]
        print(f"Foreign Keys: {fk_count}")

        cur.close(); conn.close()
        return True
    except Exception as e:
        print(f"[!] verify_setup error: {e}")
        return False

def main():
    print("🚀 ALFABOT clean setup start")
    if not create_database():
        sys.exit(1)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        print("[>] Applying clean schema with only admin user...")
        run_sql(conn, SCHEMA_SQL)
        conn.commit()
        conn.close()
        print("✅ Done.")
    except Exception as e:
        print(f"[!] setup error: {e}")
        sys.exit(1)

    ok = verify_setup()
    print("🎉 Ready - Database created with only admin user!" if ok else "⚠️ Verify had issues")


if __name__ == '__main__':
    main()