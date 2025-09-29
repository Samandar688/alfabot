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
\.


--
-- Data for Name: akt_ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.akt_ratings (id, request_id, request_type, rating, comment, created_at) FROM stdin;
\.


--
-- Data for Name: connection_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connection_orders (id, user_id, region, address, tarif_id, longitude, latitude, rating, notes, jm_notes, is_active, status, created_at, updated_at, controller_notes) FROM stdin;
\.


--
-- Data for Name: connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connections (id, sender_id, recipient_id, connecion_id, technician_id, saff_id, created_at, updated_at, sender_status, recipient_status) FROM stdin;
\.


--
-- Data for Name: material_and_technician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_and_technician (id, user_id, material_id, quantity) FROM stdin;
\.


--
-- Data for Name: material_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_requests (id, description, user_id, applications_id, material_id, connection_order_id, technician_order_id, saff_order_id, quantity, price, total_price) FROM stdin;
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, name, price, description, quantity, serial_number, created_at, updated_at) FROM stdin;
1	Switch Cisco Catalyst 2960	2500000.00	24 portli boshqariladigan switch	50	CIS-2960-24	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
2	UTP kabeli (305m)	850000.00	Cat 6 UTP internet kabeli, 305 metr	25	UTP-CAT6-305	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
3	Patch Panel 24 port	350000.00	Cat 6 uchun 24 portli patch panel	40	PP-CAT6-24	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
4	IP Telefon Grandstream GXP1610	650000.00	Oddiy ofis uchun IP telefon	75	GS-GXP1610	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
6	Router Mikrotik hAP ac2	950000.00	Kichik ofis uchun kuchli router	35	MT-HAPAC2	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
7	Access Point Ubiquiti UniFi AP AC LITE	1200000.00	Wi-Fi qamrovini kengaytirish uchun	60	UB-UAP-AC-LITE	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
8	RJ45 Konnektorlari (100 dona)	75000.00	UTP kabeli uchun konnektorlar to'plami	100	RJ45-CAT6-100	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
10	Optik Patch Cord SC-SC 3m	45000.00	Optik ulanish uchun 3 metrli kabel	150	PC-SC-SC-3M	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
11	KVM Switch 4 Port HDMI	450000.00	4 kompyuterni bitta monitor bilan boshqarish	30	KVM-HDMI-4P	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
12	SFP Module 1.25G SM	180000.00	Optik switch uchun SFP modul	125	SFP-1.25G-SM	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
13	Crimping Tool RJ45/RJ11	120000.00	Tarmoq kabelini siqish uchun asbob	50	CRIMP-RJ45-11	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
14	LAN Cable Tester	90000.00	Tarmoq kabelining ishlashini tekshirish	75	LAN-TEST-01	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
15	PoE Injector Gigabit	150000.00	IP kamera yoki Access Point uchun quvvat	90	POE-INJ-GIGA	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
16	HDD Seagate SkyHawk 1TB	550000.00	Videokuzatuv tizimlari uchun qattiq disk	40	ST1000VX005	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
17	Media Converter 10/100/1000M	220000.00	Optikani misga o'tkazgich	70	MC-GIGA-SM	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
18	Rackmount PDU 8 outlet	280000.00	Server shkafi uchun elektr taqsimlagich	25	PDU-RACK-8	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
19	Fiber Optic Cleaver	800000.00	Optik tolani aniq kesish uchun asbob	10	FOC-CLEAVER-HS	2025-09-29 10:51:22.595723	2025-09-29 10:51:22.595723
5	Server shkafi 12U	1800000.00	Devorga osiladigan server shkafi, 12U	10	SRV-SH-12U	2025-09-29 10:51:22.595723	2025-09-29 11:08:54.639825
20	Thermal Paste Arctic MX-4 (4g)	65000.00	Protsessor uchun termopasta	110	ARCTIC-MX4-4G	2025-09-29 10:51:22.595723	2025-09-29 11:09:12.202715
9	UPS APC 650VA	700000.00	Elektr uzilishlaridan himoya	30	APC-650VA	2025-09-29 10:51:22.595723	2025-09-29 11:09:29.27365
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
\.


--
-- Data for Name: smart_service_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.smart_service_orders (id, user_id, category, service_type, address, longitude, latitude, is_active, created_at, updated_at) FROM stdin;
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
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked, created_at, updated_at) FROM stdin;
71	1978574076	Улугбек	ulugbekbb	+998900042544	uz	\N	\N	client	\N	f	2025-09-29 11:45:28.533854+05	2025-09-29 11:45:38.076429+05
\.


--
-- Name: akt_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_documents_id_seq', 1, false);


--
-- Name: akt_ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_ratings_id_seq', 1, false);


--
-- Name: connection_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connection_orders_id_seq', 1, false);


--
-- Name: connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connections_id_seq', 1, false);


--
-- Name: material_and_technician_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_and_technician_id_seq', 1, false);


--
-- Name: material_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_requests_id_seq', 1, false);


--
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_seq', 20, true);


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 1, false);


--
-- Name: saff_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saff_orders_id_seq', 1, false);


--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.smart_service_orders_id_seq', 1, false);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 4, true);


--
-- Name: technician_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.technician_orders_id_seq', 1, false);


--
-- Name: user_sequential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sequential_id_seq', 71, true);


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

