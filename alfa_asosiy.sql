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
    'between_controller_technician',
    'in_call_center_operator'
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
    description_ish text,
    description_operator text
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
5	20	technician	AKT-20-20250918	documents\\AKT-20-20250918.docx	d18f8b2baa37e84100457d118af1ded752a37760464673267df65d0b7c87c9b0	2025-09-18 15:40:42.49439	2025-09-18 15:40:42.700887
6	45	connection	AKT-45-20250928	documents\\AKT-45-20250928.docx	9d570589a68b2b2c2238245f6d26fb576deee9eba9d412b3e0cded41b5927613	2025-09-28 22:25:00.549999	2025-09-28 22:25:01.208266
7	21	technician	AKT-21-20250928	documents\\AKT-21-20250928.docx	e063c09ce8dbaed359ca4bcc753bdd71576e02754875039846abf6b99d4c0728	2025-09-28 22:34:05.064702	2025-09-28 22:34:05.568977
8	43	connection	AKT-43-20250928	documents\\AKT-43-20250928.docx	f42ee7265bf9da866319d2b994b226e6bebecf1a28a1cd58bff0d9dd6319ad49	2025-09-28 22:36:38.349556	2025-09-28 22:36:38.719077
9	36	connection	AKT-36-20250928	documents\\AKT-36-20250928.docx	e33b16c442d7f9ace2f3931bc745290685a5dc19bfbdf688eee3084385d94cb6	2025-09-28 23:16:55.257354	\N
10	34	connection	AKT-34-20250928	documents\\AKT-34-20250928.docx	cd5282201f88bb2b7fea6c0bd7376718827ca15e2220bc9cee16e8fa56c1b6af	2025-09-28 23:22:30.920067	2025-09-28 23:22:31.272143
11	17	technician	AKT-17-20250928	documents\\AKT-17-20250928.docx	12bb0572f36b37a91ab9e2461f6f683f00f2ea58ea79121f8045636a14b9c58c	2025-09-28 23:25:49.8239	\N
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
35	62	toshkent shahri	Samarqand darvoza	1	\N	\N	\N	\N	\N	t	completed	2025-09-15 16:22:41.850015+05	2025-09-15 16:26:28.326709+05	
37	63	xorazm	egwrewrgewrgegr	2	\N	\N	\N	\N	\N	t	in_manager	2025-09-15 16:51:13.485613+05	2025-09-15 16:51:13.485613+05	
39	63	namangan	wergwergwergweg	1	69.267472	41.304603	\N	\N	\N	t	in_manager	2025-09-15 16:52:14.929101+05	2025-09-15 16:52:14.929101+05	
40	63	jizzax	afsfdsfsfgsdgd	3	\N	\N	\N	\N	\N	t	in_junior_manager	2025-09-15 16:52:38.254459+05	2025-09-17 14:41:04.050367+05	
38	63	qashqadaryo	erwgwergwergwergg	3	\N	\N	\N	\N	\N	t	in_junior_manager	2025-09-15 16:51:29.271218+05	2025-09-17 14:41:59.642184+05	
41	64	toshkent shahri	asdfasdfasdfas	1	\N	\N	\N	\N	\N	t	in_manager	2025-09-18 15:50:38.86373+05	2025-09-18 15:50:38.86373+05	
42	66	namangan	aaaaaaaaaaaa	1	\N	\N	\N	\N	\N	t	in_junior_manager	2025-09-22 13:59:15.16272+05	2025-09-22 13:59:15.16272+05	
44	66	namangan	aaaaaaaaaaaabbbbbcccccccccc	1	\N	\N	\N	\N	\N	t	in_junior_manager	2025-09-22 13:59:46.810481+05	2025-09-22 13:59:46.810481+05	
45	66	namangan	aaaaaaaaaaaabbbbbccccccccccdddddddddddd	1	\N	\N	\N	\N	vppopoooovpopovpop	t	completed	2025-09-22 13:59:50.690611+05	2025-09-28 22:24:59.623745+05	
43	66	namangan	aaaaaaaaaaaabbbbb	1	\N	\N	\N	\N	\N	t	completed	2025-09-22 13:59:42.114707+05	2025-09-28 22:36:37.616375+05	
46	65	namangan	btstbbtsrbetet	1	\N	\N	\N	\N	\N	t	in_junior_manager	2025-09-28 22:38:19.856315+05	2025-09-28 22:48:18.588632+05	
36	63	namangan	werfgwergwergwerg	2	\N	\N	\N	\N	bir nimada xatolik bor	t	completed	2025-09-15 16:50:57.849205+05	2025-09-28 23:16:54.316874+05	
34	62	toshkent shahri	Yunusobod	1	\N	\N	\N	\N	\N	t	completed	2025-09-15 16:06:19.034763+05	2025-09-28 23:22:30.097366+05	
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
144	63	66	40	\N	\N	2025-09-17 14:41:04.050367+05	2025-09-17 14:41:04.050367+05	in_manager	in_junior_manager
145	63	66	38	\N	\N	2025-09-17 14:41:59.642184+05	2025-09-17 14:41:59.642184+05	in_manager	in_junior_manager
146	64	64	20	\N	\N	2025-09-18 15:39:43.712114+05	2025-09-18 15:39:43.712114+05	between_controller_technician	in_technician
147	64	64	20	\N	\N	2025-09-18 15:39:47.603633+05	2025-09-18 15:39:47.603633+05	in_technician	in_technician_work
148	64	64	20	\N	\N	2025-09-18 15:40:41.954848+05	2025-09-18 15:40:41.954848+05	in_technician_work	completed
149	64	65	21	\N	\N	2025-09-18 16:00:43.836099+05	2025-09-18 16:00:43.836099+05	in_controller	between_controller_technician
151	63	63	36	\N	\N	2025-09-20 16:05:19.228547+05	2025-09-20 16:05:19.228547+05	in_manager	in_junior_manager
152	63	62	36	\N	\N	2025-09-20 16:35:26.942008+05	2025-09-20 16:35:26.942008+05	in_junior_manager	in_controller
153	63	63	42	\N	\N	2025-09-22 14:02:26.474462+05	2025-09-22 14:02:26.474462+05	in_manager	in_junior_manager
154	63	63	43	\N	\N	2025-09-22 14:03:21.2742+05	2025-09-22 14:03:21.2742+05	in_manager	in_junior_manager
155	63	63	44	\N	\N	2025-09-22 14:03:28.802332+05	2025-09-22 14:03:28.802332+05	in_manager	in_junior_manager
156	63	63	45	\N	\N	2025-09-22 14:03:32.546248+05	2025-09-22 14:03:32.546248+05	in_manager	in_junior_manager
157	63	62	43	\N	\N	2025-09-22 14:05:16.541745+05	2025-09-22 14:05:16.541745+05	in_junior_manager	in_controller
158	63	62	45	\N	\N	2025-09-22 14:07:28.251951+05	2025-09-22 14:07:28.251951+05	in_junior_manager	in_controller
159	63	65	45	\N	\N	2025-09-23 15:59:22.633889+05	2025-09-23 15:59:22.633889+05	in_controller	between_controller_technician
160	63	65	19	\N	\N	2025-09-23 16:40:43.623842+05	2025-09-23 16:40:43.623842+05	in_controller	between_controller_technician
161	63	65	43	\N	\N	2025-09-23 20:19:56.243199+05	2025-09-23 20:19:56.243199+05	in_controller	between_controller_technician
163	63	65	\N	\N	16	2025-09-24 11:04:59.662527+05	2025-09-24 11:04:59.662527+05	in_controller	between_controller_technician
164	63	65	\N	\N	15	2025-09-24 11:26:22.146946+05	2025-09-24 11:26:22.146946+05	in_controller	between_controller_technician
166	63	65	\N	\N	14	2025-09-24 11:52:19.440128+05	2025-09-24 11:52:19.440128+05	in_controller	between_controller_technician
167	63	65	\N	\N	13	2025-09-24 12:01:21.572836+05	2025-09-24 12:01:21.572836+05	in_controller	between_controller_technician
168	63	65	\N	18	\N	2025-09-24 12:01:58.210625+05	2025-09-24 12:01:58.210625+05	in_controller	between_controller_technician
169	63	65	\N	17	\N	2025-09-24 12:02:57.267403+05	2025-09-24 12:02:57.267403+05	in_controller	between_controller_technician
170	63	65	36	\N	\N	2025-09-24 12:03:19.576451+05	2025-09-24 12:03:19.576451+05	in_controller	between_controller_technician
171	63	65	\N	\N	12	2025-09-24 12:04:19.577796+05	2025-09-24 12:04:19.577796+05	in_controller	between_controller_technician
172	63	64	16	\N	\N	2025-09-24 17:03:11.780241+05	2025-09-24 17:03:11.780241+05	in_controller	in_call_center_operator
173	65	65	45	\N	\N	2025-09-28 22:24:30.929009+05	2025-09-28 22:24:30.929009+05	between_controller_technician	in_technician
174	65	65	45	\N	\N	2025-09-28 22:24:35.07289+05	2025-09-28 22:24:35.07289+05	in_technician	in_technician_work
175	65	65	45	\N	\N	2025-09-28 22:24:59.623745+05	2025-09-28 22:24:59.623745+05	in_technician_work	completed
176	65	65	21	\N	\N	2025-09-28 22:33:19.548715+05	2025-09-28 22:33:19.548715+05	between_controller_technician	in_technician
177	65	65	21	\N	\N	2025-09-28 22:33:23.829584+05	2025-09-28 22:33:23.829584+05	in_technician	in_technician_work
178	65	65	21	\N	\N	2025-09-28 22:34:04.193819+05	2025-09-28 22:34:04.193819+05	in_technician_work	completed
179	65	65	43	\N	\N	2025-09-28 22:36:08.567509+05	2025-09-28 22:36:08.567509+05	between_controller_technician	in_technician
180	65	65	43	\N	\N	2025-09-28 22:36:13.315187+05	2025-09-28 22:36:13.315187+05	in_technician	in_technician_work
181	65	65	43	\N	\N	2025-09-28 22:36:37.616375+05	2025-09-28 22:36:37.616375+05	in_technician_work	completed
182	65	66	46	\N	\N	2025-09-28 22:48:18.588632+05	2025-09-28 22:48:18.588632+05	in_manager	in_junior_manager
183	65	64	\N	22	\N	2025-09-28 22:57:29.226638+05	2025-09-28 22:57:29.226638+05	in_controller	in_call_center_operator
184	64	63	\N	\N	10	2025-09-28 23:01:47.733264+05	2025-09-28 23:01:47.733264+05	in_call_center_supervisor	in_controller
185	65	63	\N	22	\N	2025-09-28 23:12:18.867489+05	2025-09-28 23:12:18.867489+05	in_call_center_operator	completed
186	65	65	36	\N	\N	2025-09-28 23:16:21.464937+05	2025-09-28 23:16:21.464937+05	between_controller_technician	in_technician
187	65	65	36	\N	\N	2025-09-28 23:16:32.217026+05	2025-09-28 23:16:32.217026+05	in_technician	in_technician_work
188	65	65	36	\N	\N	2025-09-28 23:16:54.316874+05	2025-09-28 23:16:54.316874+05	in_technician_work	completed
189	65	65	34	\N	\N	2025-09-28 23:22:30.097366+05	2025-09-28 23:22:30.097366+05	in_technician_work	completed
190	65	65	\N	19	\N	2025-09-28 23:22:45.59501+05	2025-09-28 23:22:45.59501+05	between_controller_technician	in_technician
191	65	65	\N	19	\N	2025-09-28 23:22:49.933462+05	2025-09-28 23:22:49.933462+05	in_technician	in_technician_work
192	65	65	\N	18	\N	2025-09-28 23:23:42.701905+05	2025-09-28 23:23:42.701905+05	between_controller_technician	in_technician
193	65	65	\N	18	\N	2025-09-28 23:23:46.750059+05	2025-09-28 23:23:46.750059+05	in_technician	in_technician_work
194	65	65	\N	17	\N	2025-09-28 23:25:06.87976+05	2025-09-28 23:25:06.87976+05	between_controller_technician	in_technician
195	65	65	\N	17	\N	2025-09-28 23:25:11.394655+05	2025-09-28 23:25:11.394655+05	in_technician	in_technician_work
196	65	65	\N	17	\N	2025-09-28 23:25:48.972504+05	2025-09-28 23:25:48.972504+05	in_technician_work	completed
\.


--
-- Data for Name: material_and_technician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_and_technician (id, user_id, material_id, quantity) FROM stdin;
22	64	3	24
23	64	4	6
24	64	5	7
21	64	1	5
25	65	3	1
26	65	2	1
\.


--
-- Data for Name: material_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_requests (id, description, user_id, applications_id, material_id, connection_order_id, technician_order_id, saff_order_id, quantity, price, total_price) FROM stdin;
17	2	64	35	5	\N	\N	\N	1	0.00	0.00
18	1	64	35	4	\N	\N	\N	1	0.00	0.00
19	5	64	14	5	\N	\N	\N	1	0.00	0.00
20	11	64	15	5	\N	\N	\N	1	0.00	0.00
21	3	64	20	1	\N	\N	\N	1	0.00	0.00
22	2	65	45	2	\N	\N	\N	1	0.00	0.00
23	1	65	21	2	\N	\N	\N	1	0.00	0.00
24	\N	65	43	2	\N	\N	\N	1	120000.00	120000.00
25	\N	65	36	2	\N	\N	\N	1	120000.00	120000.00
26	\N	65	17	2	\N	\N	\N	1	120000.00	120000.00
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, name, price, description, quantity, serial_number, created_at, updated_at) FROM stdin;
1	Router TP-Link	450000.00	Uy uchun Wi-Fi router	2	RT-001	2025-09-11 11:57:50.834606	2025-09-15 16:18:42.421949
4	Modem ZTE	380000.00	Internet modem, ADSL/GPON	3	MD-202	2025-09-11 11:57:50.834606	2025-09-15 16:19:07.637541
3	Wi-Fi Adapter	90000.00	Kompyuter uchun USB Wi-Fi adapter	0	AD-101	2025-09-11 11:57:50.834606	2025-09-18 16:25:00.408564
2	Optik sim 50m	120000.00	Optik tolali internet kabel	1	SM-050	2025-09-11 11:57:50.834606	2025-09-18 16:25:41.742696
5	laan	30000.00	slomn	5	CB-005	2025-09-11 11:57:50.834606	2025-09-18 16:28:16.696261
6	dsjad	1213212.00	slfhasd af	12	\N	2025-09-18 16:30:46.780588	2025-09-18 16:30:46.780588
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (id, title, description, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: saff_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.saff_orders (id, user_id, phone, region, abonent_id, tarif_id, address, description, status, type_of_zayavka, is_active, created_at, updated_at) FROM stdin;
3	63	+998900247151	6	63	1	lakjsdfgk;lja;l		in_controller	connection	t	2025-09-17 15:30:12.877661+05	2025-09-17 15:30:12.877661+05
4	63	+998900247151	5	63	4	sdfasdf		in_controller	connection	t	2025-09-17 16:00:33.393901+05	2025-09-17 16:00:33.393901+05
5	63	+998900247151	5	63	2	asdfaaaaaaaaaaaaaa		in_controller	connection	t	2025-09-17 16:39:32.744551+05	2025-09-17 16:39:32.744551+05
6	63	+998900247151	13	63	3	aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa		in_controller	connection	t	2025-09-17 16:40:22.218264+05	2025-09-17 16:40:22.218264+05
7	63	+998900247151	1	63	\N	asdf;lasjdlfj	zor ishlamadi	in_controller	technician	t	2025-09-17 16:43:22.581652+05	2025-09-17 16:43:22.581652+05
8	63	+998900247151	14	63	\N	bbbbbbbbbbbbbbbbbb	dabdalaaaaa	in_controller	technician	t	2025-09-17 17:18:20.308124+05	2025-09-17 17:18:20.308124+05
9	63	+998912340024	5	66	3	asdfasd		in_controller	connection	t	2025-09-18 13:07:05.262442+05	2025-09-18 13:07:05.262442+05
11	63	998900042544	11	65	1	zzzzzzzzzzzzzzzzzzzzzzz		in_controller	connection	t	2025-09-19 17:34:25.71649+05	2025-09-19 17:34:25.71649+05
18	63	+998912340024	10	66	3	ssssssssssssss		between_controller_technician	connection	t	2025-09-22 15:10:11.594649+05	2025-09-23 19:20:12.746573+05
17	63	+998900247151	8	63	3	eeeeeeeeeeeeeee		between_controller_technician	connection	t	2025-09-22 15:08:46.146875+05	2025-09-23 19:20:43.286528+05
16	63	+998912340024	8	66	3	axaxaxaxa		between_controller_technician	connection	t	2025-09-22 14:10:24.68757+05	2025-09-24 11:04:59.662527+05
15	63	+998912340024	13	66	1	jhhjhjhjhjhjhjhjhjhjhjh		between_controller_technician	connection	t	2025-09-22 13:39:56.125003+05	2025-09-24 11:26:22.146946+05
14	63	+998937490211	6	62	\N	сссееыенрапр	фылдвоаж фывоаф	between_controller_technician	technician	t	2025-09-20 11:20:31.777834+05	2025-09-24 11:52:19.440128+05
13	63	+998912340024	7	66	\N	ooooooooooooop	bir nima bo'ldi	between_controller_technician	technician	t	2025-09-20 11:12:43.561916+05	2025-09-24 12:01:21.572836+05
12	63	998908200120	11	64	3	qqqqqqqqqqqqqqqqqqqqqqqq		between_controller_technician	connection	t	2025-09-20 11:01:15.426418+05	2025-09-24 12:04:19.577796+05
19	63	+998937490211	10	62	4	ooooooooooooooooooooooooooop	[conn_type:b2c]	in_controller	connection	t	2025-09-24 12:40:12.703054+05	2025-09-24 12:40:12.703054+05
20	63	+998937490211	7	62	3	ssssssssssssssssrrrrrrrrrrrrrrr	[conn_type:b2b]	in_controller	connection	t	2025-09-24 12:51:02.487697+05	2025-09-24 12:51:02.487697+05
21	63	+998937490211	12	62	2	aoao\\		in_controller	connection	t	2025-09-24 12:56:52.543545+05	2025-09-24 12:56:52.543545+05
22	63	+998937490211	4	62	\N	ggggggggggg	hammasi dabdala lkein askldj	in_controller	technician	t	2025-09-24 13:52:34.089897+05	2025-09-24 13:52:34.089897+05
23	63	+998937490211	7	62	3	tytytytyt		in_controller	connection	t	2025-09-24 14:02:46.547497+05	2025-09-24 14:02:46.547497+05
24	63	998900042544	13	65	3	dddda		in_controller	connection	t	2025-09-24 14:28:44.519621+05	2025-09-24 14:28:44.519621+05
25	63	998900042544	13	65	\N	aa	qqqqqqqqqqssssssssssss	in_controller	technician	t	2025-09-24 14:29:46.070037+05	2025-09-24 14:29:46.070037+05
26	63	998900042544	13	65	\N	a	uuuuuuuuuuu	in_controller	technician	t	2025-09-24 14:44:56.606698+05	2025-09-24 14:44:56.606698+05
27	65	+998937490211	1	62	1	gegeggzgdggd		in_controller	connection	t	2025-09-28 22:47:12.891786+05	2025-09-28 22:47:12.891786+05
28	65	+998937490211	8	62	\N	bfiwebfiewbafwifew	nvjknkvnernnvarrer	in_controller	technician	t	2025-09-28 22:47:57.680981+05	2025-09-28 22:47:57.680981+05
29	65	+998937490211	2	62	1	sjndsnvknkvnksvsvwv		in_controller	connection	t	2025-09-28 22:50:11.817057+05	2025-09-28 22:50:11.817057+05
30	65	+998937490211	9	62	1	fsdfsdfsfewffew		in_controller	connection	t	2025-09-28 22:51:38.260322+05	2025-09-28 22:51:38.260322+05
10	64	998908200120	14	64	4	asdfasdfasd		in_controller	connection	t	2025-09-18 15:54:22.245999+05	2025-09-28 23:01:47.726555+05
31	65	+998937490211	7	62	1	gregegdgddgegegeggd		in_call_center_supervisor	connection	t	2025-09-28 23:13:31.059278+05	2025-09-28 23:13:31.059278+05
\.


--
-- Data for Name: smart_service_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.smart_service_orders (id, user_id, category, service_type, address, longitude, latitude, is_active, created_at, updated_at) FROM stdin;
4	63	maxsus_qoshimcha_xizmatlar	qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash	tertreterwtresdgf	1.2e-05	57.807223	t	2025-09-15 16:53:20.835811+05	2025-09-15 16:53:20.835811+05
5	63	xavfsizlik_kuzatuv_tizimlari	yuzni_tanish_face_recognition_tizimlari	dsgdfshsdhfgdhfdghfdg	\N	\N	t	2025-09-15 16:53:35.705431+05	2025-09-15 16:53:35.705431+05
6	63	multimediya_aloqa_tizimlari	uy_kinoteatri_tizimlari_ornatish	nuanifsginsgfogf	\N	\N	t	2025-09-15 16:54:19.404242+05	2025-09-15 16:54:19.404242+05
7	63	energiya_yashil_texnologiyalar	elektr_energiyasini_tejovchi_yoritish_tizimlari	dfsgdfgdsfgdsgdfg	\N	\N	t	2025-09-15 16:57:25.113825+05	2025-09-15 16:57:25.113825+05
8	65	xavfsizlik_kuzatuv_tizimlari	yong_signalizatsiyasi_tizimlari	nkfnkdsnkfnsfnffsfsfge	\N	\N	t	2025-09-28 22:39:09.730129+05	2025-09-28 22:39:09.730129+05
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

COPY public.technician_orders (id, user_id, region, abonent_id, address, media, longitude, latitude, description, status, rating, notes, is_active, created_at, updated_at, description_ish, description_operator) FROM stdin;
14	63	1	1010170	bektemir	\N	\N	\N	sim uzildimi?	completed	\N	\N	t	2025-09-15 16:32:38.51007+05	2025-09-15 16:34:57.055377+05	Sim uzilgan ekanku?	\N
15	63	1	52	Nurafshin ko'chasi 12 uy	\N	\N	\N	wifi sim uzildi?	completed	\N	\N	t	2025-09-15 16:44:11.664919+05	2025-09-15 16:46:21.500839+05	Sim tiklash kerak boʻladi	\N
20	63	1	872298	jhasvbjakvav	\N	\N	\N	bdjsfbgdsbvdsfbvds	completed	\N	\N	t	2025-09-15 16:50:43.67177+05	2025-09-18 15:40:41.954848+05	DASDFASDFADFS	\N
16	63	1	354354354	A.Navoiy ko'chasi 113	\N	\N	\N	muammo bor anig'ini bilmayman	in_call_center_operator	\N	\N	t	2025-09-15 16:48:58.18245+05	2025-09-24 17:03:11.780241+05	\N	\N
21	64	1	1213221231321	oajsdha sdfhasdfadas	AgACAgIAAxkBAAKWF2jL493Mlz7kD3lIHGorlbE3aLkuAAKUEDIb-2hYSvwaT_fC_4CPAQADAgADeQADNgQ	\N	\N	dbnasdja aksdf ad	completed	\N	\N	t	2025-09-18 15:50:15.771293+05	2025-09-28 22:34:04.193819+05	salom	\N
22	65	1	2343242342	gsmeegggseegegg	\N	\N	\N	gndksjknjn;gan;g	completed	\N	\N	t	2025-09-28 22:38:50.494338+05	2025-09-28 23:12:18.778765+05	\N	\N
19	63	1	215254525423	qtwwwvwerwertwverw	\N	\N	\N	dfsgdfsgdfsgdfsgdfsgg	in_technician_work	\N	\N	t	2025-09-15 16:50:23.212953+05	2025-09-28 23:23:05.282343+05	xaxadafmgaeerge	\N
18	63	1	4354343432\\	dfsgfgdsdfsgdgfsgdf	\N	\N	\N	gffsgdfgdfsfsgdsgd	in_technician_work	\N	\N	t	2025-09-15 16:50:03.918087+05	2025-09-28 23:23:58.469674+05	egreggegegegg	\N
17	63	1	314223234	afgfgfigdifsgdifsggfs	\N	\N	\N	dasfgasgasgsfgn	completed	\N	\N	t	2025-09-15 16:49:42.893283+05	2025-09-28 23:25:48.972504+05	rwwtwtwtwssgs	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked, created_at, updated_at) FROM stdin;
68	8182298038	\N	\N	\N	uz	\N	\N	client	\N	f	2025-09-23 13:55:09.809163+05	2025-09-23 13:55:09.809163+05
64	2129817198	Bakirali Zokirov	bakirali_zokirov	998908200120	uz	\N	\N	callcenter_operator	\N	f	2025-09-15 16:03:11.666949+05	2025-09-24 16:14:10.989486+05
63	6217122923	Samandar Isroilov	IsroilovSamandar	+998900247151	ru	\N	\N	controller	\N	f	2025-09-15 16:01:28.704651+05	2025-09-24 17:22:15.412573+05
66	8401544590	Abdumannop	abdumuratov_off	+998912340024	uz	\N	\N	junior_manager	\N	f	2025-09-17 13:53:22.575421+05	2025-09-17 14:40:48.341458+05
67	6065251302	\N	Muhammadabdullayev2309	\N	uz	\N	\N	client	\N	f	2025-09-20 13:39:03.923394+05	2025-09-20 13:39:03.923394+05
62	7793341014	Ал-Хабаш Шейх	bakiralizokirov	+998937490211	uz	\N	\N	client	\N	f	2025-09-15 16:01:04.869427+05	2025-09-28 22:46:39.214159+05
65	1978574076	Ulug'bek	ulugbekbb	998900042544	uz	\N	\N	warehouse	\N	f	2025-09-15 16:11:18.524108+05	2025-09-28 23:26:34.850552+05
\.


--
-- Name: akt_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_documents_id_seq', 11, true);


--
-- Name: akt_ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_ratings_id_seq', 5, true);


--
-- Name: connection_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connection_orders_id_seq', 46, true);


--
-- Name: connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connections_id_seq', 196, true);


--
-- Name: material_and_technician_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_and_technician_id_seq', 26, true);


--
-- Name: material_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_requests_id_seq', 26, true);


--
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_seq', 6, true);


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 1, false);


--
-- Name: saff_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saff_orders_id_seq', 31, true);


--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.smart_service_orders_id_seq', 8, true);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 4, true);


--
-- Name: technician_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.technician_orders_id_seq', 22, true);


--
-- Name: user_sequential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sequential_id_seq', 68, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


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
-- Name: idx_conn_connecion_last; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_conn_connecion_last ON public.connections USING btree (connecion_id, created_at DESC, id DESC);


--
-- Name: idx_conn_recipient_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_conn_recipient_status ON public.connections USING btree (recipient_status);


--
-- Name: idx_conn_saff_last; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_conn_saff_last ON public.connections USING btree (saff_id, created_at DESC, id DESC);


--
-- Name: idx_conn_technician_last; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_conn_technician_last ON public.connections USING btree (technician_id, created_at DESC, id DESC);


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
-- Name: idx_saff_ccs_active_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_ccs_active_created ON public.saff_orders USING btree (created_at, id) WHERE ((status = 'in_call_center_supervisor'::public.connection_order_status) AND (is_active = true));


--
-- Name: idx_saff_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_orders_status ON public.saff_orders USING btree (status);


--
-- Name: idx_saff_orders_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_orders_user ON public.saff_orders USING btree (user_id);


--
-- Name: idx_saff_status_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_saff_status_active ON public.saff_orders USING btree (status, is_active);


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
    ADD CONSTRAINT connections_saff_id_fkey FOREIGN KEY (saff_id) REFERENCES public.saff_orders(id) ON DELETE CASCADE;


--
-- Name: connections connections_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_technician_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_technician_id_fkey FOREIGN KEY (technician_id) REFERENCES public.technician_orders(id) ON DELETE CASCADE;


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

