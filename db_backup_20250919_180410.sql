--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: connection_order_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.connection_order_status AS ENUM (
    'new',
    'in_manager',
    'in_junior_manager',
    'in_controller',
    'in_technician',
    'in_diagnostics',
    'in_repairs',
    'in_warehouse',
    'in_technician_work',
    'completed',
    'between_controller_technician',
    'in_call_center_supervisor'
);


ALTER TYPE public.connection_order_status OWNER TO postgres;

--
-- Name: smart_service_category; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.smart_service_category AS ENUM (
    'aqlli_avtomatlashtirilgan_xizmatlar',
    'xavfsizlik_kuzatuv_tizimlari',
    'internet_tarmoq_xizmatlari',
    'energiya_yashil_texnologiyalar',
    'multimediya_aloqa_tizimlari',
    'maxsus_qoshimcha_xizmatlar'
);


ALTER TYPE public.smart_service_category OWNER TO postgres;

--
-- Name: smart_service_type; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.smart_service_type AS text
	CONSTRAINT smart_service_type_check CHECK ((VALUE = ANY (ARRAY['aqlli_uy_tizimlarini_ornatish_sozlash'::text, 'aqlli_yoritish_smart_lighting_tizimlari'::text, 'aqlli_termostat_iqlim_nazarati_tizimlari'::text, 'smart_lock_internet_orqali_boshqariladigan_eshik_qulfi_tizimlari'::text, 'aqlli_rozetalar_energiya_monitoring_tizimlari'::text, 'uyni_masofadan_boshqarish_qurilmalari_yagona_uzim_orqali_boshqarish'::text, 'aqlli_pardalari_jaluz_tizimlari'::text, 'aqlli_malahiy_texnika_integratsiyasi'::text, 'videokuzatuv_kameralarini_ornatish_ip_va_analog'::text, 'kamera_arxiv_tizimlari_bulutli_saqlash_xizmatlari'::text, 'domofon_tizimlari_ornatish'::text, 'xavfsizlik_signalizatsiyasi_harakat_sensorlarini_ornatish'::text, 'yong_signalizatsiyasi_tizimlari'::text, 'gaz_sizish_sav_toshqinliqqa_qarshi_tizimlar'::text, 'yuzni_tanish_face_recognition_tizimlari'::text, 'avtomatik_eshik_darvoza_boshqaruv_tizimlari'::text, 'wi_fi_tarmoqlarini_ornatish_sozlash'::text, 'wi_fi_qamrov_zonasini_kengaytirish_access_point'::text, 'mobil_aloqa_signalini_kuchaytirish_repeater'::text, 'ofis_va_uy_uchun_lokal_tarmoq_lan_qurish'::text, 'internet_provayder_xizmatlarini_ulash'::text, 'server_va_nas_qurilmalarini_ornatish'::text, 'bulutli_fayl_almashish_zaxira_tizimlari'::text, 'vpn_va_xavfsiz_internet_ulanishlarini_tashkil_qilish'::text, 'quyosh_panellarini_ornatish_ulash'::text, 'quyosh_batareyalari_orqali_energiya_saqlash_tizimlari'::text, 'shamol_generatorlarini_ornatish'::text, 'elektr_energiyasini_tejovchi_yoritish_tizimlari'::text, 'avtomatik_suv_orish_tizimlari_smart_irrigation'::text, 'smart_tv_ornatish_ulash'::text, 'uy_kinoteatri_tizimlari_ornatish'::text, 'audio_tizimlar_multiroom'::text, 'ip_telefoniya_mini_ats_tizimlarini_tashkil_qilish'::text, 'video_konferensiya_tizimlari'::text, 'interaktiv_taqdimot_tizimlari_proyektor_led_ekran'::text, 'aqlli_ofis_tizimlarini_ornatish'::text, 'data_markaz_server_room_loyihalash_montaj_qilish'::text, 'qurilma_tizimlar_uchun_texnik_xizmat_korsatish'::text, 'dasturiy_taminotni_ornatish_yangilash'::text, 'iot_internet_of_things_qurilmalarini_integratsiya_qilish'::text, 'qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash'::text, 'suniy_intellekt_asosidagi_uy_ofis_boshqaruv_tizimlari'::text])));


ALTER DOMAIN public.smart_service_type OWNER TO postgres;

--
-- Name: technician_order_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.technician_order_status AS ENUM (
    'new',
    'in_controller',
    'in_technician',
    'in_diagnostics',
    'in_repairs',
    'in_warehouse',
    'in_technician_work',
    'completed',
    'between_controller_technician'
);


ALTER TYPE public.technician_order_status OWNER TO postgres;

--
-- Name: type_of_zayavka; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.type_of_zayavka AS ENUM (
    'connection',
    'technician'
);


ALTER TYPE public.type_of_zayavka OWNER TO postgres;

--
-- Name: user_role; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.user_role AS ENUM (
    'admin',
    'client',
    'manager',
    'junior_manager',
    'controller',
    'technician',
    'warehouse',
    'callcenter_supervisor',
    'callcenter_operator'
);


ALTER TYPE public.user_role OWNER TO postgres;

--
-- Name: create_user_sequential(bigint, text, text, text, public.user_role); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.create_user_sequential(p_telegram_id bigint, p_username text DEFAULT NULL::text, p_full_name text DEFAULT NULL::text, p_phone text DEFAULT NULL::text, p_role public.user_role DEFAULT 'client'::public.user_role) RETURNS TABLE(user_id integer, user_telegram_id bigint, user_username text, user_full_name text, user_phone text, user_role public.user_role, user_created_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_user_id INTEGER;
    ret_user_id INTEGER;
    ret_telegram_id BIGINT;
    ret_username TEXT;
    ret_full_name TEXT;
    ret_phone TEXT;
    ret_role user_role;
    ret_created_at TIMESTAMPTZ;
BEGIN
    -- Get next sequential ID
    SELECT get_next_sequential_user_id() INTO new_user_id;
    
    -- Insert user with sequential ID
    INSERT INTO users (id, telegram_id, username, full_name, phone, role)
    VALUES (new_user_id, p_telegram_id, p_username, p_full_name, p_phone, p_role)
    ON CONFLICT (telegram_id) DO UPDATE SET
        username = EXCLUDED.username,
        full_name = EXCLUDED.full_name,
        phone = EXCLUDED.phone,
        updated_at = NOW()
    RETURNING users.id, users.telegram_id, users.username, users.full_name, users.phone, users.role, users.created_at
    INTO ret_user_id, ret_telegram_id, ret_username, ret_full_name, ret_phone, ret_role, ret_created_at;
    
    create_user_sequential.user_id := ret_user_id;
    create_user_sequential.user_telegram_id := ret_telegram_id;
    create_user_sequential.user_username := ret_username;
    create_user_sequential.user_full_name := ret_full_name;
    create_user_sequential.user_phone := ret_phone;
    create_user_sequential.user_role := ret_role;
    create_user_sequential.user_created_at := ret_created_at;
    
    RETURN NEXT;
END;
$$;


ALTER FUNCTION public.create_user_sequential(p_telegram_id bigint, p_username text, p_full_name text, p_phone text, p_role public.user_role) OWNER TO postgres;

--
-- Name: FUNCTION create_user_sequential(p_telegram_id bigint, p_username text, p_full_name text, p_phone text, p_role public.user_role); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.create_user_sequential(p_telegram_id bigint, p_username text, p_full_name text, p_phone text, p_role public.user_role) IS 'Creates user with sequential ID';


--
-- Name: get_next_sequential_user_id(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_next_sequential_user_id() RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    next_id INTEGER;
BEGIN
    -- Get the next value from our custom sequence
    SELECT nextval('user_sequential_id_seq') INTO next_id;
    
    -- Check if this ID already exists in users table
    WHILE EXISTS (SELECT 1 FROM users WHERE id = next_id) LOOP
        SELECT nextval('user_sequential_id_seq') INTO next_id;
    END LOOP;
    
    RETURN next_id;
END;
$$;


ALTER FUNCTION public.get_next_sequential_user_id() OWNER TO postgres;

--
-- Name: FUNCTION get_next_sequential_user_id(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.get_next_sequential_user_id() IS 'Returns next available sequential user ID';


--
-- Name: reset_user_sequential_sequence(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.reset_user_sequential_sequence() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    max_id INTEGER;
BEGIN
    -- Get the maximum existing user ID
    SELECT COALESCE(MAX(id), 0) + 1 INTO max_id FROM users;
    
    -- Reset the sequence to start from the next available ID
    PERFORM setval('user_sequential_id_seq', max_id, false);
END;
$$;


ALTER FUNCTION public.reset_user_sequential_sequence() OWNER TO postgres;

--
-- Name: FUNCTION reset_user_sequential_sequence(); Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON FUNCTION public.reset_user_sequential_sequence() IS 'Resets sequence to match existing data';


--
-- Name: set_updated_at(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.set_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_updated_at() OWNER TO postgres;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: akt_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.akt_documents (
    id integer NOT NULL,
    request_id integer NOT NULL,
    request_type character varying(20) NOT NULL,
    akt_number character varying(50) NOT NULL,
    file_path character varying(255) NOT NULL,
    file_hash character varying(64) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    sent_to_client_at timestamp without time zone,
    CONSTRAINT akt_documents_request_type_check CHECK (((request_type)::text = ANY (ARRAY[('connection'::character varying)::text, ('technician'::character varying)::text, ('saff'::character varying)::text])))
);


ALTER TABLE public.akt_documents OWNER TO postgres;

--
-- Name: TABLE akt_documents; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.akt_documents IS 'AKT hujjatlari ma''lumotlari';


--
-- Name: COLUMN akt_documents.request_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.request_id IS 'Zayavka ID';


--
-- Name: COLUMN akt_documents.request_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.request_type IS 'Zayavka turi (connection, technician, saff)';


--
-- Name: COLUMN akt_documents.akt_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.akt_number IS 'AKT raqami (AKT-{request_id}-{YYYYMMDD})';


--
-- Name: COLUMN akt_documents.file_path; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.file_path IS 'Fayl yo''li';


--
-- Name: COLUMN akt_documents.file_hash; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.file_hash IS 'Fayl SHA256 hash';


--
-- Name: COLUMN akt_documents.sent_to_client_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_documents.sent_to_client_at IS 'Mijozga yuborilgan vaqt';


--
-- Name: akt_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.akt_documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.akt_documents_id_seq OWNER TO postgres;

--
-- Name: akt_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.akt_documents_id_seq OWNED BY public.akt_documents.id;


--
-- Name: akt_ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.akt_ratings (
    id integer NOT NULL,
    request_id integer NOT NULL,
    request_type character varying(20) NOT NULL,
    rating integer NOT NULL,
    comment text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT akt_ratings_rating_check CHECK (((rating >= 0) AND (rating <= 5))),
    CONSTRAINT akt_ratings_request_type_check CHECK (((request_type)::text = ANY (ARRAY[('connection'::character varying)::text, ('technician'::character varying)::text, ('saff'::character varying)::text])))
);


ALTER TABLE public.akt_ratings OWNER TO postgres;

--
-- Name: TABLE akt_ratings; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.akt_ratings IS 'AKT reytinglari va izohlari';


--
-- Name: COLUMN akt_ratings.request_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_ratings.request_id IS 'Zayavka ID';


--
-- Name: COLUMN akt_ratings.request_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_ratings.request_type IS 'Zayavka turi (connection, technician, saff)';


--
-- Name: COLUMN akt_ratings.rating; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_ratings.rating IS 'Reyting (1-5)';


--
-- Name: COLUMN akt_ratings.comment; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.akt_ratings.comment IS 'Mijoz izohi';


--
-- Name: akt_ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.akt_ratings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.akt_ratings_id_seq OWNER TO postgres;

--
-- Name: akt_ratings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.akt_ratings_id_seq OWNED BY public.akt_ratings.id;


--
-- Name: connection_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.connection_orders (
    id bigint NOT NULL,
    user_id bigint,
    region text,
    address text,
    tarif_id bigint,
    longitude double precision,
    latitude double precision,
    rating integer,
    notes text,
    jm_notes text,
    is_active boolean DEFAULT true NOT NULL,
    status public.connection_order_status DEFAULT 'new'::public.connection_order_status NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    controller_notes text DEFAULT ''::text NOT NULL,
    CONSTRAINT connection_orders_status_check CHECK ((status = ANY (ARRAY['in_manager'::public.connection_order_status, 'in_junior_manager'::public.connection_order_status, 'in_controller'::public.connection_order_status, 'between_controller_technician'::public.connection_order_status, 'in_technician'::public.connection_order_status, 'in_technician_work'::public.connection_order_status, 'completed'::public.connection_order_status])))
);


ALTER TABLE public.connection_orders OWNER TO postgres;

--
-- Name: connection_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.connection_orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.connection_orders_id_seq OWNER TO postgres;

--
-- Name: connection_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.connection_orders_id_seq OWNED BY public.connection_orders.id;


--
-- Name: connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.connections (
    id bigint NOT NULL,
    sender_id bigint,
    recipient_id bigint,
    connecion_id integer,
    technician_id bigint,
    saff_id bigint,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    sender_status text,
    recipient_status text
);


ALTER TABLE public.connections OWNER TO postgres;

--
-- Name: connections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.connections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.connections_id_seq OWNER TO postgres;

--
-- Name: connections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.connections_id_seq OWNED BY public.connections.id;


--
-- Name: material_and_technician; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.material_and_technician (
    id integer NOT NULL,
    user_id integer NOT NULL,
    material_id integer NOT NULL,
    quantity integer
);


ALTER TABLE public.material_and_technician OWNER TO postgres;

--
-- Name: material_and_technician_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.material_and_technician_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.material_and_technician_id_seq OWNER TO postgres;

--
-- Name: material_and_technician_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.material_and_technician_id_seq OWNED BY public.material_and_technician.id;


--
-- Name: material_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.material_requests (
    id integer NOT NULL,
    description text,
    user_id integer NOT NULL,
    applications_id integer NOT NULL,
    material_id integer NOT NULL,
    connection_order_id integer,
    technician_order_id integer,
    saff_order_id integer,
    quantity integer DEFAULT 1,
    price numeric(10,2) DEFAULT 0,
    total_price numeric(10,2) DEFAULT 0
);


ALTER TABLE public.material_requests OWNER TO postgres;

--
-- Name: material_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.material_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.material_requests_id_seq OWNER TO postgres;

--
-- Name: material_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.material_requests_id_seq OWNED BY public.material_requests.id;


--
-- Name: materials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materials (
    id integer NOT NULL,
    name character varying(255),
    price numeric(10,2),
    description text,
    quantity integer DEFAULT 0,
    serial_number character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.materials OWNER TO postgres;

--
-- Name: materials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.materials_id_seq OWNER TO postgres;

--
-- Name: materials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materials_id_seq OWNED BY public.materials.id;


--
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    id integer NOT NULL,
    title text NOT NULL,
    description text,
    created_by bigint,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- Name: TABLE reports; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.reports IS 'Stores reports created by managers for various purposes';


--
-- Name: reports_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_id_seq OWNER TO postgres;

--
-- Name: reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.id;


--
-- Name: saff_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.saff_orders (
    id bigint NOT NULL,
    user_id bigint,
    phone text,
    region integer,
    abonent_id text,
    tarif_id bigint,
    address text,
    description text,
    status public.connection_order_status DEFAULT 'in_call_center_supervisor'::public.connection_order_status NOT NULL,
    type_of_zayavka public.type_of_zayavka DEFAULT 'connection'::public.type_of_zayavka NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.saff_orders OWNER TO postgres;

--
-- Name: saff_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.saff_orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.saff_orders_id_seq OWNER TO postgres;

--
-- Name: saff_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.saff_orders_id_seq OWNED BY public.saff_orders.id;


--
-- Name: smart_service_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.smart_service_orders (
    id bigint NOT NULL,
    user_id bigint,
    category public.smart_service_category NOT NULL,
    service_type public.smart_service_type NOT NULL,
    address text NOT NULL,
    longitude double precision,
    latitude double precision,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.smart_service_orders OWNER TO postgres;

--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.smart_service_orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.smart_service_orders_id_seq OWNER TO postgres;

--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.smart_service_orders_id_seq OWNED BY public.smart_service_orders.id;


--
-- Name: tarif; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tarif (
    id bigint NOT NULL,
    name text,
    picture text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tarif OWNER TO postgres;

--
-- Name: tarif_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tarif_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tarif_id_seq OWNER TO postgres;

--
-- Name: tarif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tarif_id_seq OWNED BY public.tarif.id;


--
-- Name: technician_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.technician_orders (
    id bigint NOT NULL,
    user_id bigint,
    region integer,
    abonent_id text,
    address text,
    media text,
    longitude double precision,
    latitude double precision,
    description text,
    status public.technician_order_status DEFAULT 'new'::public.technician_order_status NOT NULL,
    rating integer,
    notes text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    description_ish text
);


ALTER TABLE public.technician_orders OWNER TO postgres;

--
-- Name: technician_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.technician_orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.technician_orders_id_seq OWNER TO postgres;

--
-- Name: technician_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.technician_orders_id_seq OWNED BY public.technician_orders.id;


--
-- Name: user_sequential_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_sequential_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_sequential_id_seq OWNER TO postgres;

--
-- Name: SEQUENCE user_sequential_id_seq; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON SEQUENCE public.user_sequential_id_seq IS 'Sequential ID generator for users table';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    telegram_id bigint,
    full_name text,
    username text,
    phone text,
    language character varying(5) DEFAULT 'uz'::character varying NOT NULL,
    region integer,
    address text,
    role public.user_role,
    abonent_id text,
    is_blocked boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: akt_documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_documents ALTER COLUMN id SET DEFAULT nextval('public.akt_documents_id_seq'::regclass);


--
-- Name: akt_ratings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_ratings ALTER COLUMN id SET DEFAULT nextval('public.akt_ratings_id_seq'::regclass);


--
-- Name: connection_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connection_orders ALTER COLUMN id SET DEFAULT nextval('public.connection_orders_id_seq'::regclass);


--
-- Name: connections id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections ALTER COLUMN id SET DEFAULT nextval('public.connections_id_seq'::regclass);


--
-- Name: material_and_technician id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician ALTER COLUMN id SET DEFAULT nextval('public.material_and_technician_id_seq'::regclass);


--
-- Name: material_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests ALTER COLUMN id SET DEFAULT nextval('public.material_requests_id_seq'::regclass);


--
-- Name: materials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials ALTER COLUMN id SET DEFAULT nextval('public.materials_id_seq'::regclass);


--
-- Name: reports id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN id SET DEFAULT nextval('public.reports_id_seq'::regclass);


--
-- Name: saff_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saff_orders ALTER COLUMN id SET DEFAULT nextval('public.saff_orders_id_seq'::regclass);


--
-- Name: smart_service_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.smart_service_orders ALTER COLUMN id SET DEFAULT nextval('public.smart_service_orders_id_seq'::regclass);


--
-- Name: tarif id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif ALTER COLUMN id SET DEFAULT nextval('public.tarif_id_seq'::regclass);


--
-- Name: technician_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.technician_orders ALTER COLUMN id SET DEFAULT nextval('public.technician_orders_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: akt_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.akt_documents (id, request_id, request_type, akt_number, file_path, file_hash, created_at, sent_to_client_at) FROM stdin;
1	30	connection	AKT-30-20250915	documents\\AKT-30-20250915.docx	b328929268c94ff4c9f2998d3af696f1e656b838cdb8b19270d824c6d7b57fd6	2025-09-15 15:35:32.199283	2025-09-15 15:35:32.379662
2	35	connection	AKT-35-20250915	documents\\AKT-35-20250915.docx	2cc01984ab37185b1346e6953ad97beb5617e9646e9cc6ba594885b0e148d26e	2025-09-15 16:26:29.140556	2025-09-15 16:26:29.44777
3	14	technician	AKT-14-20250915	documents\\AKT-14-20250915.docx	3d1a095dafbc2e15a289439a43fbdc48798cc06e83b4534c7910079fce060b13	2025-09-15 16:34:57.848292	2025-09-15 16:34:58.215354
4	15	technician	AKT-15-20250915	documents\\AKT-15-20250915.docx	8067b3787b1342af4ff967ab733f14b5f825ada159df6b0d1cda297198deed3a	2025-09-15 16:46:22.271715	2025-09-15 16:46:22.493341
\.


--
-- Data for Name: akt_ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.akt_ratings (id, request_id, request_type, rating, comment, created_at) FROM stdin;
1	35	connection	5	X	2025-09-15 16:28:06.251149
3	14	technician	4	\N	2025-09-15 16:35:45.927107
4	15	technician	4	x	2025-09-15 16:46:55.648805
\.


--
-- Data for Name: connection_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connection_orders (id, user_id, region, address, tarif_id, longitude, latitude, rating, notes, jm_notes, is_active, status, created_at, updated_at, controller_notes) FROM stdin;
34	62	toshkent shahri	Yunusobod	1	\N	\N	\N	\N	\N	t	in_technician_work	2025-09-15 16:06:19.034763+05	2025-09-15 16:16:18.168799+05	
35	62	toshkent shahri	Samarqand darvoza	1	\N	\N	\N	\N	\N	t	completed	2025-09-15 16:22:41.850015+05	2025-09-15 16:26:28.326709+05	
36	63	namangan	werfgwergwergwerg	2	\N	\N	\N	\N	\N	t	in_manager	2025-09-15 16:50:57.849205+05	2025-09-15 16:50:57.849205+05	
37	63	xorazm	egwrewrgewrgegr	2	\N	\N	\N	\N	\N	t	in_manager	2025-09-15 16:51:13.485613+05	2025-09-15 16:51:13.485613+05	
38	63	qashqadaryo	erwgwergwergwergg	3	\N	\N	\N	\N	\N	t	in_manager	2025-09-15 16:51:29.271218+05	2025-09-15 16:51:29.271218+05	
39	63	namangan	wergwergwergweg	1	69.267472	41.304603	\N	\N	\N	t	in_manager	2025-09-15 16:52:14.929101+05	2025-09-15 16:52:14.929101+05	
40	63	jizzax	afsfdsfsfgsdgd	3	\N	\N	\N	\N	\N	t	in_manager	2025-09-15 16:52:38.254459+05	2025-09-15 16:52:38.254459+05	
\.


--
-- Data for Name: connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connections (id, sender_id, recipient_id, connecion_id, technician_id, saff_id, created_at, updated_at, sender_status, recipient_status) FROM stdin;
124	63	64	34	\N	\N	2025-09-15 16:06:55.227498+05	2025-09-15 16:06:55.227498+05	in_manager	in_junior_manager
125	64	65	34	\N	\N	2025-09-15 16:12:29.009015+05	2025-09-15 16:12:29.009015+05	in_junior_manager	in_controller
126	65	64	34	\N	\N	2025-09-15 16:14:18.020977+05	2025-09-15 16:14:18.020977+05	in_controller	between_controller_technician
127	64	64	34	\N	\N	2025-09-15 16:16:15.025202+05	2025-09-15 16:16:15.025202+05	between_controller_technician	in_technician
128	64	64	34	\N	\N	2025-09-15 16:16:18.168799+05	2025-09-15 16:16:18.168799+05	in_technician	in_technician_work
129	63	62	35	\N	\N	2025-09-15 16:24:16.772582+05	2025-09-15 16:24:16.772582+05	in_manager	in_junior_manager
130	62	63	35	\N	\N	2025-09-15 16:25:22.038905+05	2025-09-15 16:25:22.038905+05	in_junior_manager	in_controller
131	63	64	35	\N	\N	2025-09-15 16:25:36.626575+05	2025-09-15 16:25:36.626575+05	in_controller	between_controller_technician
132	64	64	35	\N	\N	2025-09-15 16:25:52.793862+05	2025-09-15 16:25:52.793862+05	between_controller_technician	in_technician
133	64	64	35	\N	\N	2025-09-15 16:25:55.622411+05	2025-09-15 16:25:55.622411+05	in_technician	in_technician_work
134	64	64	35	\N	\N	2025-09-15 16:26:28.326709+05	2025-09-15 16:26:28.326709+05	in_technician_work	completed
135	62	64	14	\N	\N	2025-09-15 16:33:45.173008+05	2025-09-15 16:33:45.173008+05	in_controller	between_controller_technician
136	64	64	14	\N	\N	2025-09-15 16:34:08.403336+05	2025-09-15 16:34:08.403336+05	between_controller_technician	in_technician
137	64	64	14	\N	\N	2025-09-15 16:34:11.109071+05	2025-09-15 16:34:11.109071+05	in_technician	in_technician_work
138	64	64	14	\N	\N	2025-09-15 16:34:57.055377+05	2025-09-15 16:34:57.055377+05	in_technician_work	completed
139	62	64	15	\N	\N	2025-09-15 16:44:38.091054+05	2025-09-15 16:44:38.091054+05	in_controller	between_controller_technician
140	64	64	15	\N	\N	2025-09-15 16:45:03.054622+05	2025-09-15 16:45:03.054622+05	between_controller_technician	in_technician
141	64	64	15	\N	\N	2025-09-15 16:45:06.589148+05	2025-09-15 16:45:06.589148+05	in_technician	in_technician_work
142	64	64	15	\N	\N	2025-09-15 16:46:21.500839+05	2025-09-15 16:46:21.500839+05	in_technician_work	completed
143	62	64	20	\N	\N	2025-09-15 17:07:39.550574+05	2025-09-15 17:07:39.550574+05	in_controller	between_controller_technician
1	3	6	1	6	1	2025-09-17 14:33:56.123669+05	2025-09-19 14:33:56.123669+05	sent	received
2	4	7	2	7	2	2025-09-18 14:33:56.123669+05	2025-09-19 14:33:56.123669+05	sent	pending
3	5	8	3	8	3	2025-09-14 14:33:56.123669+05	2025-09-17 14:33:56.123669+05	completed	completed
4	3	6	4	6	4	2025-09-19 11:33:56.123669+05	2025-09-19 14:33:56.123669+05	sent	in_progress
5	12	11	5	\N	5	2025-09-19 13:33:56.123669+05	2025-09-19 14:33:56.123669+05	sent	pending
\.


--
-- Data for Name: material_and_technician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_and_technician (id, user_id, material_id, quantity) FROM stdin;
1	6	1	3
2	6	4	5
3	6	8	10
4	7	2	2
5	7	6	1
6	7	13	4
7	8	3	1
8	8	7	1
9	8	11	1
\.


--
-- Data for Name: material_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_requests (id, description, user_id, applications_id, material_id, connection_order_id, technician_order_id, saff_order_id, quantity, price, total_price) FROM stdin;
17	2	64	35	5	\N	\N	\N	1	0.00	0.00
18	1	64	35	4	\N	\N	\N	1	0.00	0.00
19	5	64	14	5	\N	\N	\N	1	0.00	0.00
20	11	64	15	5	\N	\N	\N	1	0.00	0.00
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, name, price, description, quantity, serial_number, created_at, updated_at) FROM stdin;
2	Optik sim 50m	120000.00	Optik tolali internet kabel	5	SM-050	2025-09-11 11:57:50.834606	2025-09-15 15:32:00.661611
1	Router TP-Link	450000.00	Uy uchun Wi-Fi router	2	RT-001	2025-09-11 11:57:50.834606	2025-09-15 16:18:42.421949
3	Wi-Fi Adapter	90000.00	Kompyuter uchun USB Wi-Fi adapter	1	AD-101	2025-09-11 11:57:50.834606	2025-09-15 16:18:54.435041
4	Modem ZTE	380000.00	Internet modem, ADSL/GPON	3	MD-202	2025-09-11 11:57:50.834606	2025-09-15 16:19:07.637541
5	LAN Kabel 5m	30000.00	Ethernet kabel, 5 metr	5	CB-005	2025-09-11 11:57:50.834606	2025-09-15 16:21:00.599566
6	Router TP-Link Archer C6	350000.00	Wi-Fi router 1200 Mbps, 4 antenna	25	RTR-001-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
7	Modem ADSL ZTE	180000.00	ADSL modem for internet connection	15	MDM-002-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
8	Switch 8-port Gigabit	420000.00	8-port Gigabit Ethernet switch	12	SWT-003-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
9	ONT Huawei HG8245H	280000.00	Optical Network Terminal GPON	30	ONT-004-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
10	Wi-Fi Extender	150000.00	Wi-Fi signal extender/repeater	8	EXT-005-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
11	UTP Cable Cat6 (100m)	85000.00	Category 6 UTP cable roll 100 meters	50	CBL-006-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
12	Fiber Optic Cable (1km)	1200000.00	Single mode fiber optic cable 1km	5	FOC-007-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
13	RJ45 Connector (100pcs)	25000.00	RJ45 connectors pack of 100 pieces	20	RJ45-008-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
14	Coaxial Cable RG6 (100m)	95000.00	RG6 coaxial cable for TV/Internet	18	COX-009-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
15	Crimping Tool RJ45	65000.00	Professional RJ45 crimping tool	6	CRM-010-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
16	Cable Tester	120000.00	Network cable tester for UTP/STP	4	TST-011-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
17	Drill Bits Set	45000.00	Set of drill bits for installation	10	DRL-012-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
18	Wall Mount Bracket	35000.00	Universal wall mount for equipment	22	MNT-013-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
19	Splitter 1:8	75000.00	1 to 8 optical splitter	3	SPL-014-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
20	Patch Cord 3m	15000.00	3 meter patch cord cable	2	PCH-015-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
21	Media Converter	250000.00	Fiber to Ethernet media converter	0	MCV-016-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
22	Optical Attenuator	180000.00	Variable optical attenuator	0	ATT-017-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
23	Fiber Optik Kabel 100m	2500000.00	Yuqori sifatli fiber optik kabel 100m	15	FOK-018-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
24	Network Switch 24-port	1500000.00	24 portli tarmoq kommutatori	8	NSW-019-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
25	WiFi Router AC1200	450000.00	Simsiz internet routeri AC1200	12	WFR-020-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
26	Ethernet Cable Cat6 50m	180000.00	Cat6 ethernet kabeli 50m	20	ETC-021-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
27	Power Adapter 12V 2A	80000.00	Quvvat adaptori 12V 2A	30	PWA-022-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
28	Antenna Yagi 15dBi	350000.00	Yonaltirilgan antenna 15dBi	6	ANT-023-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
29	Coaxial Cable RG6 100m	220000.00	Koaksial kabel RG6 100m	14	COX-024-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
30	Signal Amplifier 20dB	650000.00	Signal kuchaytirgichi 20dB	4	SIG-025-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
31	Test Low Stock Item 1	100000.00	Past qoldiq test mahsuloti 1	5	TLS-026-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
32	Test Low Stock Item 2	150000.00	Past qoldiq test mahsuloti 2	3	TLS-027-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
33	Test Low Stock Item 3	200000.00	Past qoldiq test mahsuloti 3	8	TLS-028-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
34	Test Out of Stock Item 1	250000.00	Tugagan test mahsuloti 1	0	TOS-029-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
35	Test Out of Stock Item 2	300000.00	Tugagan test mahsuloti 2	0	TOS-030-2024	2025-09-19 14:33:56.099305	2025-09-19 14:33:56.099305
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (id, title, description, created_by, created_at, updated_at) FROM stdin;
1	Kunlik hisobot	Bugungi kun boyicha umumiy statistika	111111111	2025-09-18 14:33:56.125662+05	2025-09-18 14:33:56.125662+05
2	Haftalik material hisoboti	Hafta davomida ishlatilingan materiallar	999999999	2025-09-12 14:33:56.125662+05	2025-09-12 14:33:56.125662+05
3	Texnik xizmat hisoboti	Texnik xizmatlar boyicha hisobot	666666666	2025-09-16 14:33:56.125662+05	2025-09-16 14:33:56.125662+05
4	Mijozlar reytingi	Mijozlar tomonidan berilgan reytinglar	333333333	2025-09-17 14:33:56.125662+05	2025-09-17 14:33:56.125662+05
5	AylД±k umumiy hisobot	Oy davomida amalga oshirilgan ishlar	111111111	2025-08-20 14:33:56.125662+05	2025-08-20 14:33:56.125662+05
\.


--
-- Data for Name: saff_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.saff_orders (id, user_id, phone, region, abonent_id, tarif_id, address, description, status, type_of_zayavka, is_active, created_at, updated_at) FROM stdin;
33	1	+998901234567	1	1001	1	Chilonzor tumani, 45-uy	Internet ulanishi sozlamasi kerak	new	connection	t	2025-01-19 14:00:00+05	2025-01-19 14:00:00+05
34	3	+998912345678	2	1002	2	Registon ko'chasi, 12-uy	Router o'rnatish talab qilinadi	in_manager	connection	t	2025-01-18 09:30:00+05	2025-01-18 09:30:00+05
35	5	+998933456789	3	1003	3	Alpomish mahallasi, 5-uy	Yangi internet liniyasi o'tkazish kerak	in_controller	connection	t	2025-01-17 11:15:00+05	2025-01-18 10:00:00+05
36	6	+998944567890	4	1004	4	Yuksalish ko'chasi, 33-uy	Fiber optik kabel o'rnatish	in_technician	connection	t	2025-01-16 15:20:00+05	2025-01-17 12:00:00+05
37	14	+998957890123	5	1005	1	Navoiy prospekti, 8-uy	Yangi tarifga o'tish uchun so'rov	completed	connection	f	2025-01-15 10:45:00+05	2025-01-16 14:30:00+05
38	6	+998966789012	1	1006	2	Mirzo Ulug'bek tumani, 22-uy	Internet tezligi past, tekshirish kerak	new	technician	t	2025-01-19 16:20:00+05	2025-01-19 16:20:00+05
39	7	+998977890123	2	1007	3	Shayxontohur tumani, 67-uy	Kabel uzilgan, almashtirish kerak	in_diagnostics	technician	t	2025-01-18 13:45:00+05	2025-01-19 08:15:00+05
40	8	+998988901234	3	1008	4	Bektemir tumani, 15-uy	Router ishlamayapti, ta'mirlash kerak	in_repairs	technician	t	2025-01-17 12:30:00+05	2025-01-18 14:20:00+05
41	9	+998999012345	4	1009	1	Sergeli tumani, 89-uy	Signal kuchsiz, antennani sozlash kerak	in_technician_work	technician	t	2025-01-16 09:10:00+05	2025-01-17 16:45:00+05
42	11	+998901112233	5	1010	2	Yunusobod tumani, 34-uy	Modem almashtirish kerak	completed	technician	f	2025-01-15 14:25:00+05	2025-01-16 11:30:00+05
43	12	+998902223344	1	1011	3	Olmazor tumani, 56-uy	Wi-Fi signali kuchsiz	in_warehouse	technician	t	2025-01-19 11:00:00+05	2025-01-19 11:00:00+05
44	13	+998903334455	2	1012	4	Yashnobod tumani, 78-uy	Yangi ulanish kerak	between_controller_technician	connection	t	2025-01-18 15:30:00+05	2025-01-19 09:45:00+05
45	62	+998904445566	3	1013	1	Uchtepa tumani, 23-uy	Internet uzilib qoladi	in_call_center_supervisor	technician	t	2025-01-17 08:15:00+05	2025-01-17 08:15:00+05
46	63	+998905556677	4	1014	2	Hamza tumani, 45-uy	Tarif o'zgartirish kerak	in_junior_manager	connection	t	2025-01-16 13:20:00+05	2025-01-17 10:30:00+05
47	64	+998906667788	5	1015	3	Qo'yliq tumani, 67-uy	Kabel ta'mirlash	in_manager	technician	t	2025-01-15 16:40:00+05	2025-01-16 12:15:00+05
\.


--
-- Data for Name: smart_service_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.smart_service_orders (id, user_id, category, service_type, address, longitude, latitude, is_active, created_at, updated_at) FROM stdin;
4	63	maxsus_qoshimcha_xizmatlar	qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash	tertreterwtresdgf	1.2e-05	57.807223	t	2025-09-15 16:53:20.835811+05	2025-09-15 16:53:20.835811+05
5	63	xavfsizlik_kuzatuv_tizimlari	yuzni_tanish_face_recognition_tizimlari	dsgdfshsdhfgdhfdghfdg	\N	\N	t	2025-09-15 16:53:35.705431+05	2025-09-15 16:53:35.705431+05
6	63	multimediya_aloqa_tizimlari	uy_kinoteatri_tizimlari_ornatish	nuanifsginsgfogf	\N	\N	t	2025-09-15 16:54:19.404242+05	2025-09-15 16:54:19.404242+05
7	63	energiya_yashil_texnologiyalar	elektr_energiyasini_tejovchi_yoritish_tizimlari	dfsgdfgdsfgdsgdfg	\N	\N	t	2025-09-15 16:57:25.113825+05	2025-09-15 16:57:25.113825+05
\.


--
-- Data for Name: tarif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarif (id, name, picture, created_at, updated_at) FROM stdin;
1	Hammasi birga 4	\N	2025-09-04 10:52:21.158691+05	2025-09-04 10:52:21.158691+05
2	Hammasi birga 3+	\N	2025-09-04 10:52:21.158691+05	2025-09-04 10:52:21.158691+05
3	Hammasi birga 3	\N	2025-09-04 10:52:21.158691+05	2025-09-04 10:52:21.158691+05
4	Hammasi birga 2	\N	2025-09-04 10:52:21.158691+05	2025-09-04 10:52:21.158691+05
\.


--
-- Data for Name: technician_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.technician_orders (id, user_id, region, abonent_id, address, media, longitude, latitude, description, status, rating, notes, is_active, created_at, updated_at, description_ish) FROM stdin;
14	63	1	1010170	bektemir	\N	\N	\N	sim uzildimi?	completed	\N	\N	t	2025-09-15 16:32:38.51007+05	2025-09-15 16:34:57.055377+05	Sim uzilgan ekanku?
15	63	1	52	Nurafshin ko'chasi 12 uy	\N	\N	\N	wifi sim uzildi?	completed	\N	\N	t	2025-09-15 16:44:11.664919+05	2025-09-15 16:46:21.500839+05	Sim tiklash kerak boʻladi
16	63	1	354354354	A.Navoiy ko'chasi 113	\N	\N	\N	muammo bor anig'ini bilmayman	in_controller	\N	\N	t	2025-09-15 16:48:58.18245+05	2025-09-15 16:48:58.18245+05	\N
17	63	1	314223234	afgfgfigdifsgdifsggfs	\N	\N	\N	dasfgasgasgsfgn	in_controller	\N	\N	t	2025-09-15 16:49:42.893283+05	2025-09-15 16:49:42.893283+05	\N
18	63	1	4354343432\\	dfsgfgdsdfsgdgfsgdf	\N	\N	\N	gffsgdfgdfsfsgdsgd	in_controller	\N	\N	t	2025-09-15 16:50:03.918087+05	2025-09-15 16:50:03.918087+05	\N
19	63	1	215254525423	qtwwwvwerwertwverw	\N	\N	\N	dfsgdfsgdfsgdfsgdfsgg	in_controller	\N	\N	t	2025-09-15 16:50:23.212953+05	2025-09-15 16:50:23.212953+05	\N
20	63	1	872298	jhasvbjakvav	\N	\N	\N	bdjsfbgdsbvdsfbvds	between_controller_technician	\N	\N	t	2025-09-15 16:50:43.67177+05	2025-09-15 17:07:39.550574+05	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked, created_at, updated_at) FROM stdin;
64	2129817198	Bakirali	bakirali_zokirov	998908200120	uz	\N	\N	technician	\N	f	2025-09-15 16:03:11.666949+05	2025-09-15 16:13:58.075917+05
65	1978574076	Ulug'bek	ulugbekbb	998900042544	uz	\N	\N	admin	\N	f	2025-09-15 16:11:18.524108+05	2025-09-15 16:14:41.284063+05
62	7793341014	Ал-Хабаш Шейх	bakiralizokirov	+998937490211	uz	\N	\N	controller	\N	f	2025-09-15 16:01:04.869427+05	2025-09-15 16:33:13.743196+05
63	6217122923	Samandar Isroilov	IsroilovSamandar	+998900247151	uz	\N	\N	admin	\N	f	2025-09-15 16:01:28.704651+05	2025-09-16 12:25:44.975547+05
1	111111111	Admin Adminov	admin_user	+998901234567	uz	1	Toshkent, Chilonzor tumani	admin	ADM001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
2	222222222	РђРґРјРёРЅ РђРґРјРёРЅРѕРІ	admin_ru	+998901234568	ru	1	РўР°С€РєРµРЅС‚, Р§РёР»Р°РЅР·Р°СЂСЃРєРёР№ СЂР°Р№РѕРЅ	admin	ADM002	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
3	333333333	Manager Managerov	manager_user	+998901234569	uz	1	Toshkent, Yunusobod tumani	manager	MNG001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
4	444444444	РњРµРЅРµРґР¶РµСЂ РњРµРЅРµРґР¶РµСЂРѕРІ	manager_ru	+998901234570	ru	2	РЎР°РјР°СЂРєР°РЅРґ, С†РµРЅС‚СЂР°Р»СЊРЅС‹Р№ СЂР°Р№РѕРЅ	manager	MNG002	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
5	555555555	Junior Manager Juniorov	jm_user	+998901234571	uz	1	Toshkent, Mirzo Ulugbek tumani	junior_manager	JMG001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
6	666666666	Technician Technicov	tech_user	+998901234572	uz	1	Toshkent, Shayxontohur tumani	technician	TCH001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
7	777777777	РўРµС…РЅРёРє РўРµС…РЅРёРєРѕРІ	tech_ru	+998901234573	ru	2	РЎР°РјР°СЂРєР°РЅРґ, РЎРёР°Р±СЃРєРёР№ СЂР°Р№РѕРЅ	technician	TCH002	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
8	888888888	Technician Warehouse	tech_warehouse	+998901234574	uz	3	Buxoro, Markaz tumani	technician	TCH003	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
9	999999999	Warehouse Manager	warehouse_user	+998901234575	uz	1	Toshkent, Sergeli tumani	warehouse	WRH001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
10	1010101010	РЎРєР»Р°Рґ РњРµРЅРµРґР¶РµСЂ	warehouse_ru	+998901234576	ru	1	РўР°С€РєРµРЅС‚, РЎРµСЂРіРµР»РёР№СЃРєРёР№ СЂР°Р№РѕРЅ	warehouse	WRH002	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
11	1111111111	Call Center Operator	call_center_operator	+998901234577	uz	1	Toshkent, Olmazor tumani	callcenter_operator	CCO001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
12	1212121212	Call Center Supervisor	callcenter_supervisor	+998901234578	uz	1	Toshkent, Bektemir tumani	callcenter_supervisor	CCS001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
13	1313131313	Controller User	controller_user	+998901234579	uz	1	Toshkent, Yashnobod tumani	controller	CTR001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
14	1414141414	Client Clientov	client_user	+998901234580	uz	1	Toshkent, Hamza tumani, 15-uy	client	CLT001	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
15	1515151515	РљР»РёРµРЅС‚ РљР»РёРµРЅС‚РѕРІ	client_ru	+998901234581	ru	2	РЎР°РјР°СЂРєР°РЅРґ, СѓР». Р РµРіРёСЃС‚Р°РЅ, 25	client	CLT002	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
16	1616161616	Client Test User	client_test	+998901234582	uz	3	Buxoro, Kogon tumani, 8-uy	client	CLT003	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
17	1717171717	Client Premium	client_premium	+998901234583	uz	1	Toshkent, Mirobod tumani, 45-uy	client	CLT004	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
18	1818181818	Client Business	client_business	+998901234584	ru	4	РќР°РјР°РЅРіР°РЅ, С†РµРЅС‚СЂР°Р»СЊРЅС‹Р№ СЂР°Р№РѕРЅ, 12	client	CLT005	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
19	1919191919	Client VIP	client_vip	+998901234585	uz	1	Toshkent, Yunusobod tumani, 88-uy	client	CLT006	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
20	2020202020	Client Corporate	client_corp	+998901234586	ru	2	РЎР°РјР°СЂРєР°РЅРґ, СѓР». РђРјРёСЂР° РўРµРјСѓСЂР°, 15	client	CLT007	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
21	2121212121	Client Standard	client_std	+998901234587	uz	3	Buxoro, Shofirkon tumani, 22-uy	client	CLT008	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
22	2222222222	Client Economy	client_eco	+998901234588	uz	4	Namangan, Pop tumani, 33-uy	client	CLT009	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
23	2323232323	Client Enterprise	client_ent	+998901234589	ru	5	РђРЅРґРёР¶Р°РЅ, С†РµРЅС‚СЂР°Р»СЊРЅС‹Р№ СЂР°Р№РѕРЅ, 44	client	CLT010	f	2025-09-19 14:33:56.085201+05	2025-09-19 14:33:56.085201+05
66	8188731606	Ibroximberk	ibrohim_fx01	+998881249327	uz	\N	\N	manager	\N	f	2025-09-19 15:17:50.921985+05	2025-09-19 15:18:34.087422+05
\.


--
-- Name: akt_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_documents_id_seq', 4, true);


--
-- Name: akt_ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_ratings_id_seq', 4, true);


--
-- Name: connection_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connection_orders_id_seq', 40, true);


--
-- Name: connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connections_id_seq', 143, true);


--
-- Name: material_and_technician_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_and_technician_id_seq', 9, true);


--
-- Name: material_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_requests_id_seq', 20, true);


--
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_seq', 35, true);


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 5, true);


--
-- Name: saff_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saff_orders_id_seq', 47, true);


--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.smart_service_orders_id_seq', 7, true);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 4, true);


--
-- Name: technician_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.technician_orders_id_seq', 20, true);


--
-- Name: user_sequential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sequential_id_seq', 66, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 65, true);


--
-- Name: akt_documents akt_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_documents
    ADD CONSTRAINT akt_documents_pkey PRIMARY KEY (id);


--
-- Name: akt_documents akt_documents_request_id_request_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_documents
    ADD CONSTRAINT akt_documents_request_id_request_type_key UNIQUE (request_id, request_type);


--
-- Name: akt_ratings akt_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_ratings
    ADD CONSTRAINT akt_ratings_pkey PRIMARY KEY (id);


--
-- Name: akt_ratings akt_ratings_request_id_request_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_ratings
    ADD CONSTRAINT akt_ratings_request_id_request_type_key UNIQUE (request_id, request_type);


--
-- Name: connection_orders connection_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connection_orders
    ADD CONSTRAINT connection_orders_pkey PRIMARY KEY (id);


--
-- Name: connections connections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_pkey PRIMARY KEY (id);


--
-- Name: material_and_technician material_and_technician_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT material_and_technician_pkey PRIMARY KEY (id);


--
-- Name: material_requests material_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_pkey PRIMARY KEY (id);


--
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);


--
-- Name: materials materials_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_serial_number_key UNIQUE (serial_number);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- Name: saff_orders saff_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saff_orders
    ADD CONSTRAINT saff_orders_pkey PRIMARY KEY (id);


--
-- Name: smart_service_orders smart_service_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.smart_service_orders
    ADD CONSTRAINT smart_service_orders_pkey PRIMARY KEY (id);


--
-- Name: tarif tarif_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif
    ADD CONSTRAINT tarif_pkey PRIMARY KEY (id);


--
-- Name: technician_orders technician_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.technician_orders
    ADD CONSTRAINT technician_orders_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_telegram_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_id_key UNIQUE (telegram_id);


--
-- Name: material_and_technician ux_mat_tech_user_material; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT ux_mat_tech_user_material UNIQUE (user_id, material_id);


--
-- Name: CONSTRAINT ux_mat_tech_user_material ON material_and_technician; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT ux_mat_tech_user_material ON public.material_and_technician IS 'Ensures unique combination of user_id and material_id for UPSERT operations';


--
-- Name: material_requests ux_material_requests_user_app_material; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT ux_material_requests_user_app_material UNIQUE (user_id, applications_id, material_id);


--
-- Name: CONSTRAINT ux_material_requests_user_app_material ON material_requests; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT ux_material_requests_user_app_material ON public.material_requests IS 'Ensures unique combination of user_id, applications_id and material_id for UPSERT operations';


--
-- Name: idx_akt_documents_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_documents_created ON public.akt_documents USING btree (created_at DESC);


--
-- Name: idx_akt_documents_request; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_documents_request ON public.akt_documents USING btree (request_id, request_type);


--
-- Name: idx_akt_documents_sent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_documents_sent ON public.akt_documents USING btree (sent_to_client_at);


--
-- Name: idx_akt_ratings_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_ratings_created ON public.akt_ratings USING btree (created_at DESC);


--
-- Name: idx_akt_ratings_rating; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_ratings_rating ON public.akt_ratings USING btree (rating);


--
-- Name: idx_akt_ratings_request; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_akt_ratings_request ON public.akt_ratings USING btree (request_id, request_type);


--
-- Name: idx_connection_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connection_orders_status ON public.connection_orders USING btree (status);


--
-- Name: idx_connection_orders_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connection_orders_user ON public.connection_orders USING btree (user_id);


--
-- Name: idx_connections_recipient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connections_recipient_id ON public.connections USING btree (recipient_id);


--
-- Name: idx_connections_sender_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connections_sender_id ON public.connections USING btree (sender_id);


--
-- Name: idx_material_requests_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_material_requests_user ON public.material_requests USING btree (user_id);


--
-- Name: idx_materials_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_materials_name ON public.materials USING btree (name);


--
-- Name: idx_materials_serial; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_materials_serial ON public.materials USING btree (serial_number);


--
-- Name: idx_reports_created_by; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_reports_created_by ON public.reports USING btree (created_by);


--
-- Name: idx_saff_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_orders_status ON public.saff_orders USING btree (status);


--
-- Name: idx_saff_orders_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_orders_user ON public.saff_orders USING btree (user_id);


--
-- Name: idx_sso_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sso_category ON public.smart_service_orders USING btree (category);


--
-- Name: idx_sso_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sso_created ON public.smart_service_orders USING btree (created_at);


--
-- Name: idx_sso_created_desc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sso_created_desc ON public.smart_service_orders USING btree (created_at DESC);


--
-- Name: idx_sso_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sso_user_id ON public.smart_service_orders USING btree (user_id);


--
-- Name: idx_technician_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_technician_orders_status ON public.technician_orders USING btree (status);


--
-- Name: idx_technician_orders_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_technician_orders_user ON public.technician_orders USING btree (user_id);


--
-- Name: idx_users_abonent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_abonent_id ON public.users USING btree (abonent_id);


--
-- Name: idx_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_id ON public.users USING btree (id);


--
-- Name: idx_users_telegram_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_telegram_id ON public.users USING btree (telegram_id);


--
-- Name: ux_material_requests_triplet; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ux_material_requests_triplet ON public.material_requests USING btree (user_id, applications_id, material_id);


--
-- Name: smart_service_orders smart_service_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER smart_service_orders_updated_at BEFORE UPDATE ON public.smart_service_orders FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: connection_orders trg_connection_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_connection_orders_updated_at BEFORE UPDATE ON public.connection_orders FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: connections trg_connections_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_connections_updated_at BEFORE UPDATE ON public.connections FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: saff_orders trg_saff_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_saff_orders_updated_at BEFORE UPDATE ON public.saff_orders FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: tarif trg_tarif_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_tarif_updated_at BEFORE UPDATE ON public.tarif FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: technician_orders trg_technician_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_technician_orders_updated_at BEFORE UPDATE ON public.technician_orders FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: users trg_users_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


--
-- Name: materials update_materials_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_materials_updated_at BEFORE UPDATE ON public.materials FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: connection_orders connection_orders_tarif_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connection_orders
    ADD CONSTRAINT connection_orders_tarif_id_fkey FOREIGN KEY (tarif_id) REFERENCES public.tarif(id) ON DELETE SET NULL;


--
-- Name: connection_orders connection_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connection_orders
    ADD CONSTRAINT connection_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_saff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_saff_id_fkey FOREIGN KEY (saff_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_technician_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_technician_id_fkey FOREIGN KEY (technician_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: material_requests fk_material_requests_connection_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT fk_material_requests_connection_order FOREIGN KEY (connection_order_id) REFERENCES public.connection_orders(id);


--
-- Name: material_requests fk_material_requests_material_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT fk_material_requests_material_id FOREIGN KEY (material_id) REFERENCES public.materials(id);


--
-- Name: material_requests fk_material_requests_saff_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT fk_material_requests_saff_order FOREIGN KEY (saff_order_id) REFERENCES public.saff_orders(id);


--
-- Name: material_requests fk_material_requests_technician_order; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT fk_material_requests_technician_order FOREIGN KEY (technician_order_id) REFERENCES public.technician_orders(id);


--
-- Name: material_and_technician material_and_technician_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT material_and_technician_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.materials(id);


--
-- Name: material_and_technician material_and_technician_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT material_and_technician_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: material_requests material_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reports reports_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(telegram_id) ON DELETE SET NULL;


--
-- Name: saff_orders saff_orders_tarif_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saff_orders
    ADD CONSTRAINT saff_orders_tarif_id_fkey FOREIGN KEY (tarif_id) REFERENCES public.tarif(id) ON DELETE SET NULL;


--
-- Name: saff_orders saff_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saff_orders
    ADD CONSTRAINT saff_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: smart_service_orders smart_service_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.smart_service_orders
    ADD CONSTRAINT smart_service_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: technician_orders technician_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.technician_orders
    ADD CONSTRAINT technician_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

