#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALFABOT Database Setup Script
Ushbu skript ma'lumotlar bazasini 0dan ko'taradi va barcha kerakli jadvallarni yaratadi.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'ulugbek202', 
    'database': 'alfa_db_uz_1'
}

def create_database():
    """Ma'lumotlar bazasini yaratish"""
    try:
        # PostgreSQL serverga ulanish (database nomisiz)
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Database mavjudligini tekshirish
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_CONFIG['database']}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"Database '{DB_CONFIG['database']}' yaratildi")
        else:
            print(f"Database '{DB_CONFIG['database']}' allaqachon mavjud")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database yaratishda xatolik: {e}")
        return False
    
    return True

def execute_sql_script():
    """SQL skriptni bajarish"""
    
    sql_script = """
-- =========================
-- ALFABOT DATABASE SETUP
-- Ma'lumotlar bazasini 0dan ko'tarish
-- =========================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- ENUM TYPES
-- =========================

-- User roles
CREATE TYPE user_role AS ENUM (
    'admin', 'client', 'manager', 'junior_manager', 'controller',
    'technician', 'warehouse', 'callcenter_supervisor', 'callcenter_operator'
);

-- Connection order statuses
CREATE TYPE connection_order_status AS ENUM (
    'new', 'in_manager', 'in_junior_manager', 'in_controller', 'in_technician',
    'in_diagnostics', 'in_repairs', 'in_warehouse', 'in_technician_work', 
    'completed', 'in_call_center'
);

-- Technician order statuses
CREATE TYPE technician_order_status AS ENUM (
    'new', 'in_controller', 'in_technician', 'in_diagnostics', 'in_repairs',
    'in_warehouse', 'in_technician_work', 'completed'
);

-- Saff order statuses
CREATE TYPE saff_order_status AS ENUM (
    'in_call_center', 'in_manager', 'in_controller', 'in_technician',
    'completed', 'cancelled'
);

-- Type of applications
CREATE TYPE type_of_zayavka AS ENUM ('connection', 'technician');

-- Smart service categories
CREATE TYPE smart_service_category AS ENUM (
    'internet', 'tv', 'phone', 'other'
);

-- =========================
-- TRIGGER FUNCTIONS
-- =========================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =========================
-- MAIN TABLES
-- =========================

-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    full_name TEXT,
    username TEXT,
    phone TEXT,
    language VARCHAR(5) NOT NULL DEFAULT 'uz',
    region INTEGER,
    address TEXT,
    role user_role,
    abonent_id TEXT,
    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tarif table
CREATE TABLE tarif (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    picture TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Connection orders
CREATE TABLE connection_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    region TEXT,
    address TEXT,
    tarif_id BIGINT REFERENCES tarif(id) ON DELETE SET NULL,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    rating INTEGER,
    notes TEXT,
    jm_notes TEXT,
    controller_notes TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    status connection_order_status NOT NULL DEFAULT 'new',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Technician orders
CREATE TABLE technician_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    region INTEGER,
    abonent_id TEXT,
    address TEXT,
    media TEXT,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    description TEXT,
    description_ish TEXT,
    status technician_order_status NOT NULL DEFAULT 'new',
    rating INTEGER,
    notes TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Saff orders
CREATE TABLE saff_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    phone TEXT,
    region INTEGER,
    abonent_id TEXT,
    tarif_id BIGINT REFERENCES tarif(id) ON DELETE SET NULL,
    address TEXT,
    description TEXT,
    status saff_order_status NOT NULL DEFAULT 'in_call_center',
    type_of_zayavka type_of_zayavka NOT NULL DEFAULT 'connection',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Connections
CREATE TABLE connections (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    recipient_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    connecion_id INTEGER,
    technician_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    saff_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    sender_status TEXT,
    recipient_status TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Smart service orders
CREATE TABLE smart_service_orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
    category smart_service_category NOT NULL,
    service_type TEXT NOT NULL,
    address TEXT NOT NULL,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Materials
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price NUMERIC,
    description TEXT,
    quantity INTEGER DEFAULT 0,
    serial_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Material and technician relationship
CREATE TABLE material_and_technician (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    quantity INTEGER,
    CONSTRAINT ux_mat_tech_user_material UNIQUE (user_id, material_id)
);

-- Material requests
CREATE TABLE material_requests (
    id SERIAL PRIMARY KEY,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    applications_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    connection_order_id INTEGER REFERENCES connection_orders(id) ON DELETE SET NULL,
    technician_order_id INTEGER REFERENCES technician_orders(id) ON DELETE SET NULL,
    saff_order_id INTEGER REFERENCES saff_orders(id) ON DELETE SET NULL,
    quantity INTEGER DEFAULT 1,
    price NUMERIC DEFAULT 0,
    total_price NUMERIC DEFAULT 0,
    CONSTRAINT ux_material_requests_user_app_material UNIQUE (user_id, applications_id, material_id)
);

-- Reports
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    created_by BIGINT REFERENCES users(telegram_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- AKT documents
CREATE TABLE akt_documents (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL,
    request_type VARCHAR(20) NOT NULL,
    akt_number VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sent_to_client_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT akt_documents_request_id_request_type_key UNIQUE (request_id, request_type)
);

-- AKT ratings
CREATE TABLE akt_ratings (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL,
    request_type VARCHAR(20) NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT akt_ratings_request_id_request_type_key UNIQUE (request_id, request_type)
);

-- =========================
-- INDEXES
-- =========================

-- Users indexes
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_abonent_id ON users(abonent_id);

-- Connection orders indexes
CREATE INDEX idx_connection_orders_user ON connection_orders(user_id);
CREATE INDEX idx_connection_orders_status ON connection_orders(status);

-- Technician orders indexes
CREATE INDEX idx_technician_orders_user ON technician_orders(user_id);
CREATE INDEX idx_technician_orders_status ON technician_orders(status);

-- Saff orders indexes
CREATE INDEX idx_saff_orders_user ON saff_orders(user_id);
CREATE INDEX idx_saff_orders_status ON saff_orders(status);

-- Connections indexes
CREATE INDEX idx_connections_sender_id ON connections(sender_id);
CREATE INDEX idx_connections_recipient_id ON connections(recipient_id);

-- Smart service orders indexes
CREATE INDEX idx_sso_user_id ON smart_service_orders(user_id);
CREATE INDEX idx_sso_category ON smart_service_orders(category);
CREATE INDEX idx_sso_created ON smart_service_orders(created_at);
CREATE INDEX idx_sso_created_desc ON smart_service_orders(created_at DESC);

-- Materials indexes
CREATE INDEX idx_materials_name ON materials(name);
CREATE INDEX idx_materials_serial ON materials(serial_number);

-- Material requests indexes
CREATE INDEX idx_material_requests_user ON material_requests(user_id);

-- Reports indexes
CREATE INDEX idx_reports_created_by ON reports(created_by);

-- AKT documents indexes
CREATE INDEX idx_akt_documents_request ON akt_documents(request_id, request_type);
CREATE INDEX idx_akt_documents_created ON akt_documents(created_at DESC);
CREATE INDEX idx_akt_documents_sent ON akt_documents(sent_to_client_at);

-- AKT ratings indexes
CREATE INDEX idx_akt_ratings_request ON akt_ratings(request_id, request_type);
CREATE INDEX idx_akt_ratings_rating ON akt_ratings(rating);
CREATE INDEX idx_akt_ratings_created ON akt_ratings(created_at DESC);

-- =========================
-- TRIGGERS
-- =========================

-- Auto-update updated_at triggers
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

CREATE TRIGGER trg_smart_service_orders_updated_at
    BEFORE UPDATE ON smart_service_orders
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_reports_updated_at
    BEFORE UPDATE ON reports
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- =========================
-- SAMPLE DATA
-- =========================

-- Insert sample tariffs
INSERT INTO tarif (name) VALUES 
    ('Hammasi birga 4'),
    ('Hammasi birga 3+'),
    ('Hammasi birga 3'),
    ('Hammasi birga 2')
ON CONFLICT DO NOTHING;

-- Insert sample materials
INSERT INTO materials (name, price, description, quantity, serial_number) VALUES
    ('Optik kabel 1km', 50000, 'Optik tolali kabel', 100, 'OPT-001'),
    ('Router TP-Link', 150000, 'Wi-Fi router', 50, 'RTR-001'),
    ('Modem ADSL', 120000, 'ADSL modem', 30, 'MDM-001'),
    ('Splitter', 25000, 'Telefon splitter', 200, 'SPL-001'),
    ('Ethernet kabel 10m', 15000, 'UTP kabel', 500, 'ETH-001')
ON CONFLICT (serial_number) DO NOTHING;

-- Insert admin user (default)
INSERT INTO users (telegram_id, full_name, username, phone_number, language, role) VALUES
    (1978574076, 'Ulugbek', 'ulugbekbb', '998900042544', 'uz', 'admin')
ON CONFLICT (telegram_id) DO NOTHING;

COMMIT;
"""
    
    try:
        # Ma'lumotlar bazasiga ulanish
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # SQL skriptni bajarish
        cursor.execute(sql_script)
        conn.commit()
        
        print("Barcha jadvallar muvaffaqiyatli yaratildi!")
        print("Indexlar qo'shildi!")
        print("Triggerlar o'rnatildi!")
        print("Boshlang'ich ma'lumotlar qo'shildi!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"SQL skript bajarishda xatolik: {e}")
        return False

def verify_setup():
    """Setup natijasini tekshirish"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Jadvallar sonini tekshirish
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]
        
        print(f"Yaratilgan jadvallar soni: {table_count}")
        
        # Jadvallar ro'yxatini ko'rsatish
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print("Yaratilgan jadvallar:")
        for table in tables:
            print(f"   {table[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Tekshirishda xatolik: {e}")
        return False

def main():
    """Asosiy funksiya"""
    print("ALFABOT Database Setup boshlandi...")
    print("=" * 50)
    
    # 1. Database yaratish
    if not create_database():
        return
    
    # 2. SQL skriptni bajarish
    if not execute_sql_script():
        return
    
    # 3. Natijani tekshirish
    if not verify_setup():
        return
    
    print("=" * 50)
    print("ALFABOT Database muvaffaqiyatli o'rnatildi!")
    print("Endi botni ishga tushirishingiz mumkin.")

if __name__ == "__main__":
    main()