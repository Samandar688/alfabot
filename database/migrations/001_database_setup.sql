-- =========================
-- ENUM TYPES
-- =========================
CREATE TYPE user_role AS ENUM (
  'admin','client','manager','junior_manager','controller',
  'technician','warehouse','callcenter_supervisor','callcenter_operator'
);

CREATE TYPE connection_order_status AS ENUM (
  'new','in_manager','in_junior_manager','in_controller','in_technician',
  'in_diagnostics','in_repairs','in_warehouse','in_technician_work','completed'
);

CREATE TYPE technician_order_status AS ENUM (
  'new','in_controller','in_technician','in_diagnostics','in_repairs',
  'in_warehouse','in_technician_work','completed'
);

CREATE TYPE type_of_zayavka AS ENUM ('connection','technician');

-- =========================
-- TRIGGER FUNCTION
-- =========================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =========================
-- TABLES
-- =========================

-- Users (from @dataclass Users)
CREATE TABLE IF NOT EXISTS users (
  id           BIGSERIAL PRIMARY KEY,
  telegram_id  BIGINT UNIQUE,
  full_name    TEXT,
  username     TEXT,
  phone        TEXT,
  language     VARCHAR(5) NOT NULL DEFAULT 'uz',
  region       INTEGER,
  address      TEXT,
  role         user_role,           
  abonent_id   TEXT,
  is_blocked   BOOLEAN NOT NULL DEFAULT FALSE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tarif (from @dataclass Tarif)
CREATE TABLE IF NOT EXISTS tarif (
  id          BIGSERIAL PRIMARY KEY,
  name        TEXT,
  picture     TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ConnectionApplication (from @dataclass ConnectionApplication)
CREATE TABLE IF NOT EXISTS connection_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES users(id) ON DELETE SET NULL,
  region       TEXT,
  address      TEXT,
  tarif_id     BIGINT REFERENCES tarif(id) ON DELETE SET NULL,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  rating       INTEGER,
  notes        TEXT,
  jm_notes     TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  status       connection_order_status NOT NULL DEFAULT 'new',
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- TechnicianApplication (from @dataclass TechnicianApplication)
CREATE TABLE IF NOT EXISTS technician_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES users(id) ON DELETE SET NULL,
  region       INTEGER,
  abonent_id   TEXT,
  address      TEXT,
  media        TEXT,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  description  TEXT,
  status       technician_order_status NOT NULL DEFAULT 'new',
  rating       INTEGER,
  notes        TEXT,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- SaffApplication (from @dataclass SaffApplication)
CREATE TABLE IF NOT EXISTS saff_orders (
  id              BIGSERIAL PRIMARY KEY,
  user_id         BIGINT REFERENCES users(id) ON DELETE SET NULL,
  phone           TEXT,
  region          INTEGER,
  abonent_id      TEXT,
  tarif_id        BIGINT REFERENCES tarif(id) ON DELETE SET NULL,
  address         TEXT,
  description     TEXT,
  status          connection_order_status NOT NULL DEFAULT 'new',
  type_of_zayavka type_of_zayavka NOT NULL DEFAULT 'connection',
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Connection (from @dataclass Connection)
CREATE TABLE IF NOT EXISTS connections (
  id              BIGSERIAL PRIMARY KEY,
  user_id         BIGINT REFERENCES users(id) ON DELETE SET NULL,
  sender_id       BIGINT REFERENCES users(id) ON DELETE SET NULL,
  recipient_id    BIGINT REFERENCES users(id) ON DELETE SET NULL,
  connecion_id    INTEGER,
  technician_id   BIGINT REFERENCES users(id) ON DELETE SET NULL,
  saff_id         BIGINT REFERENCES users(id) ON DELETE SET NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_users_telegram_id        ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_abonent_id         ON users(abonent_id);
CREATE INDEX IF NOT EXISTS idx_connection_orders_user   ON connection_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_connection_orders_status ON connection_orders(status);
CREATE INDEX IF NOT EXISTS idx_technician_orders_user   ON technician_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_technician_orders_status ON technician_orders(status);
CREATE INDEX IF NOT EXISTS idx_saff_orders_user         ON saff_orders(user_id);
CREATE INDEX IF NOT EXISTS idx_saff_orders_status       ON saff_orders(status);

-- =========================
-- TRIGGERS (auto-update updated_at)
-- =========================
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_tarif_updated_at
BEFORE UPDATE ON tarif
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_connection_orders_updated_at
BEFORE UPDATE ON connection_orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_technician_orders_updated_at
BEFORE UPDATE ON technician_orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_saff_orders_updated_at
BEFORE UPDATE ON saff_orders
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_connections_updated_at
BEFORE UPDATE ON connections
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- SAMPLE DATA
-- =========================

-- Insert sample tariffs (from connection_order.py)
INSERT INTO tarif (name) VALUES 
    ('Hammasi birga 4'),
    ('Hammasi birga 3+'),
    ('Hammasi birga 3'),
    ('Hammasi birga 2')
ON CONFLICT DO NOTHING;