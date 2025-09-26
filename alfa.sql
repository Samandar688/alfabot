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
    'in_manager',
    'in_junior_manager',
    'in_controller',
    'in_technician',
    'in_diagnostics',
    'in_repairs',
    'in_warehouse',
    'in_technician_work',
    'completed',
    'in_call_center',
    'in_call_center_operator',
    'in_call_center_supervisor',
    'between_controller_technician'
);


ALTER TYPE public.connection_order_status OWNER TO postgres;

--
-- Name: saff_order_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.saff_order_status AS ENUM (
    'in_call_center',
    'in_manager',
    'in_controller',
    'in_warehouse',
    'in_technician',
    'in_technician_work',
    'completed',
    'cancelled',
    'between_controller_technician'
);


ALTER TYPE public.saff_order_status OWNER TO postgres;

--
-- Name: smart_service_category; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.smart_service_category AS ENUM (
    'aqlli_avtomatlashtirilgan_xizmatlar',
    'umnye_avtomatizirovannye_uslugi',
    'xavfsizlik_kuzatuv_tizimlari',
    'sistemy_bezopasnosti_nablyudeniya',
    'internet_tarmoq_xizmatlari',
    'internet_setevye_uslugi',
    'energiya_yashil_texnologiyalar',
    'energiya_zelenye_texnologii',
    'multimediya_aloqa_tizimlari',
    'multimedia_sistemy_svyazi',
    'maxsus_qoshimcha_xizmatlar',
    'specialnye_dopolnitelnye_uslugi'
);


ALTER TYPE public.smart_service_category OWNER TO postgres;

--
-- Name: TYPE smart_service_category; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TYPE public.smart_service_category IS 'Bilingual (UZ/RU)';


--
-- Name: smart_service_type; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.smart_service_type AS text
	CONSTRAINT smart_service_type_check CHECK ((VALUE = ANY (ARRAY['aqlli_uy_tizimlarini_ornatish_sozlash'::text, 'aqlli_yoritish_smart_lighting_tizimlari'::text, 'aqlli_termostat_iqlim_nazarati_tizimlari'::text, 'smart_lock_internet_boshqariladigan_eshik_qulfi'::text, 'aqlli_rozetalar_energiya_monitoring_tizimlari'::text, 'uyni_masofadan_boshqarish_qurilmalari_uzim'::text, 'aqlli_pardalari_jaluz_tizimlari'::text, 'aqlli_malahiy_texnika_integratsiyasi'::text, 'videokuzatuv_kameralarini_ornatish_ip_va_analog'::text, 'kamera_arxiv_tizimlari_bulutli_saqlash_xizmatlari'::text, 'domofon_tizimlari_ornatish'::text, 'xavfsizlik_signalizatsiyasi_harakat_sensorlari'::text, 'yong_signalizatsiyasi_tizimlari'::text, 'gaz_sizish_sav_toshqinliqqa_qarshi_tizimlar'::text, 'yuzni_tanish_face_recognition_tizimlari'::text, 'avtomatik_eshik_darvoza_boshqaruv_tizimlari'::text, 'wi_fi_tarmoqlarini_ornatish_sozlash'::text, 'wi_fi_qamrov_zonasini_kengaytirish_access_point'::text, 'mobil_aloqa_signalini_kuchaytirish_repeater'::text, 'ofis_va_uy_uchun_lokal_tarmoq_lan_qurish'::text, 'internet_provayder_xizmatlarini_ulash'::text, 'server_va_nas_qurilmalarini_ornatish'::text, 'bulutli_fayl_almashish_zaxira_tizimlari'::text, 'vpn_va_xavfsiz_internet_ulanishlarini_tashkil'::text, 'quyosh_panellarini_ornatish_ulash'::text, 'quyosh_batareyalari_orqali_energiya_saqlash'::text, 'shamol_generatorlarini_ornatish'::text, 'elektr_energiyasini_tejovchi_yoritish_tizimlari'::text, 'avtomatik_suv_orish_tizimlari_smart_irrigation'::text, 'smart_tv_ornatish_ulash'::text, 'uy_kinoteatri_tizimlari_ornatish'::text, 'audio_tizimlar_multiroom'::text, 'ip_telefoniya_mini_ats_tizimlarini_tashkil'::text, 'video_konferensiya_tizimlari'::text, 'interaktiv_taqdimot_tizimlari_proyektor_led'::text, 'aqlli_ofis_tizimlarini_ornatish'::text, 'data_markaz_server_room_loyihalash_montaj'::text, 'qurilma_tizimlar_uchun_texnik_xizmat_korsatish'::text, 'dasturiy_taminotni_ornatish_yangilash'::text, 'iot_internet_of_things_qurilmalarini_integratsiya'::text, 'qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash'::text, 'suniy_intellekt_asosidagi_uy_ofis_boshqaruv'::text, 'ustanovka_nastroyka_sistem_umnogo_doma'::text, 'umnoe_osveshchenie_smart_lighting_sistemy'::text, 'umnyy_termostat_sistemy_klimat_kontrolya'::text, 'smart_lock_internet_upravlyaemyy_zamok_dveri'::text, 'umnye_rozetki_sistemy_monitoring_energii'::text, 'distantsionnoe_upravlenie_domom_ustroystv'::text, 'umnye_shtory_zhalyuzi_sistemy'::text, 'integratsiya_umnoy_bytovoy_texniki'::text, 'ustanovka_kamer_videonablyudeniya_ip_analog'::text, 'sistemy_arxiva_kamer_oblachnoe_xranenie'::text, 'ustanovka_sistem_domofona'::text, 'oxrannaya_signalizatsiya_datchiki_dvizheniya'::text, 'pozharnaya_signalizatsiya_sistemy'::text, 'sistemy_protiv_utechki_gaza_vody_potopa'::text, 'sistemy_raspoznavaniya_lits_face_recognition'::text, 'avtomaticheskie_sistemy_upravleniya_dver_vorot'::text, 'ustanovka_nastroyka_wi_fi_setey'::text, 'rasshirenie_zony_pokrytiya_wi_fi_access_point'::text, 'usilenie_signala_mobilnoy_svyazi_repeater'::text, 'postroenie_lokalnoy_seti_lan_dlya_ofisa_doma'::text, 'podklyuchenie_uslug_internet_provaydera'::text, 'ustanovka_serverov_nas_ustroystv'::text, 'oblachnye_sistemy_obmena_rezervnogo_kopir'::text, 'organizatsiya_vpn_bezopasnyx_internet_soedineniy'::text, 'ustanovka_podklyuchenie_solnechnyx_paneley'::text, 'nakoplenie_energii_cherez_solnechnye_batarei'::text, 'ustanovka_vetryanyx_generatorov'::text, 'energosberegayushchie_sistemy_osveshcheniya'::text, 'avtomaticheskie_sistemy_poliva_smart_irrigation'::text, 'ustanovka_podklyuchenie_smart_tv'::text, 'ustanovka_sistem_domashnego_kinoteatr'::text, 'audio_sistemy_multiroom'::text, 'organizatsiya_ip_telefonii_mini_ats_sistem'::text, 'sistemy_videokonferentsiy'::text, 'interaktivnye_prezentatsionnye_sistemy_proyektor_led'::text, 'ustanovka_sistem_umnogo_ofisa'::text, 'proektirovanie_montazh_data_tsentr_server_room'::text, 'texnicheskoe_obsluzhivanie_ustroystv_sistem'::text, 'ustanovka_obnovlenie_programmnogo_obespecheniya'::text, 'integratsiya_iot_internet_of_things_ustroystv'::text, 'nastroyka_sistem_distantsionnogo_upravleniya_ustroystv'::text, 'upravlenie_domom_ofisom_na_osnove_ii'::text])));


ALTER DOMAIN public.smart_service_type OWNER TO postgres;

--
-- Name: DOMAIN smart_service_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON DOMAIN public.smart_service_type IS '42 bilingual service types';


--
-- Name: technician_order_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.technician_order_status AS ENUM (
    'in_controller',
    'in_technician',
    'in_diagnostics',
    'in_repairs',
    'in_warehouse',
    'in_technician_work',
    'completed',
    'cancelled',
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
-- Name: normalize_sso_category(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.normalize_sso_category(p_cat text) RETURNS public.smart_service_category
    LANGUAGE plpgsql IMMUTABLE
    AS $$
BEGIN
  CASE p_cat
    WHEN 'umnye_avtomatizirovannye_uslugi' THEN RETURN 'aqlli_avtomatlashtirilgan_xizmatlar'::public.smart_service_category;
    WHEN 'sistemy_bezopasnosti_nablyudeniya' THEN RETURN 'xavfsizlik_kuzatuv_tizimlari'::public.smart_service_category;
    WHEN 'internet_setevye_uslugi' THEN RETURN 'internet_tarmoq_xizmatlari'::public.smart_service_category;
    WHEN 'energiya_zelenye_texnologii' THEN RETURN 'energiya_yashil_texnologiyalar'::public.smart_service_category;
    WHEN 'multimedia_sistemy_svyazi' THEN RETURN 'multimediya_aloqa_tizimlari'::public.smart_service_category;
    WHEN 'specialnye_dopolnitelnye_uslugi' THEN RETURN 'maxsus_qoshimcha_xizmatlar'::public.smart_service_category;
    ELSE RETURN p_cat::public.smart_service_category;
  END CASE;
END;
$$;


ALTER FUNCTION public.normalize_sso_category(p_cat text) OWNER TO postgres;

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
-- Name: trg_normalize_sso_category(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_normalize_sso_category() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.category := public.normalize_sso_category(NEW.category::TEXT);
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.trg_normalize_sso_category() OWNER TO postgres;

--
-- Name: trg_sync_connections_ids(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_sync_connections_ids() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.connection_order_id IS NOT NULL AND NEW.connecion_id IS NULL THEN
    NEW.connecion_id := NEW.connection_order_id::INTEGER;
  ELSIF NEW.connecion_id IS NOT NULL AND NEW.connection_order_id IS NULL THEN
    NEW.connection_order_id := NEW.connecion_id::BIGINT;
  END IF;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.trg_sync_connections_ids() OWNER TO postgres;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = NOW();
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
    created_at timestamp with time zone DEFAULT now(),
    sent_to_client_at timestamp with time zone
);


ALTER TABLE public.akt_documents OWNER TO postgres;

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
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.akt_ratings OWNER TO postgres;

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
    controller_notes text DEFAULT ''::text NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    status public.connection_order_status DEFAULT 'in_manager'::public.connection_order_status NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
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
    connection_order_id bigint,
    technician_id bigint,
    saff_id bigint,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    sender_status text,
    recipient_status text,
    connecion_id integer
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
    quantity integer DEFAULT 0
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
    price numeric DEFAULT 0,
    total_price numeric DEFAULT 0
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
    price numeric,
    description text,
    quantity integer DEFAULT 0,
    serial_number character varying(100),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
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
    status public.saff_order_status DEFAULT 'in_call_center'::public.saff_order_status NOT NULL,
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
    description_ish text,
    description_operator text,
    status public.technician_order_status DEFAULT 'in_controller'::public.technician_order_status NOT NULL,
    rating integer,
    notes text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
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
1	1	connection	AKT-001	/docs/akt1.pdf	abc123	2025-09-24 16:58:36.098947+05	\N
2	13	connection	AKT-13-20250926	documents\\AKT-13-20250926.docx	e36b0bbb939ca772a2bcbdd8acf66d644bbcd871219931924ac1946551b32785	2025-09-26 16:06:36.24867+05	2025-09-26 16:06:36.539279+05
3	11	technician	AKT-11-20250926	documents\\AKT-11-20250926.docx	ceb9585f459b578dd5b0355e737e66042d1a63de417cc7146d481368078c04b7	2025-09-26 16:17:39.595537+05	2025-09-26 16:17:39.7652+05
\.


--
-- Data for Name: akt_ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.akt_ratings (id, request_id, request_type, rating, comment, created_at) FROM stdin;
1	1	connection	5	\N	2025-09-24 16:58:36.098947+05
2	13	connection	5	Nice	2025-09-26 16:08:18.439926+05
\.


--
-- Data for Name: connection_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connection_orders (id, user_id, region, address, tarif_id, longitude, latitude, rating, notes, jm_notes, controller_notes, is_active, status, created_at, updated_at) FROM stdin;
2	\N	Toshkent	Toshkent sh., Chilonzor t., 1-uy	1	69.240562	41.311081	\N	Yangi ulanish kerak	Texnik ko'rik o'tkazildi		t	in_warehouse	2025-09-24 15:01:01.15963+05	2025-09-24 17:01:01.15963+05
3	\N	Samarqand	Samarqand sh., Registon ko'ch., 15-uy	2	66.975681	39.627012	\N	Internet ulanishi kerak	Hujjatlar tayyor		t	in_warehouse	2025-09-23 17:01:01.15963+05	2025-09-24 17:01:01.15963+05
4	\N	Buxoro	Buxoro sh., Mustaqillik ko'ch., 25-uy	3	64.585262	39.767477	\N	Tezkor ulanish so'ralmoqda	Barcha tekshiruvlar tugallandi		t	in_warehouse	2025-09-24 14:01:01.15963+05	2025-09-24 17:01:01.15963+05
5	\N	Andijon	Andijon sh., Navoi ko'ch., 10-uy	1	72.344415	40.78237	\N	Uyga internet o'rnatish	Materiallar tayyor		t	in_warehouse	2025-09-24 16:31:01.15963+05	2025-09-24 17:01:01.15963+05
6	\N	Farg'ona	Farg'ona sh., Mustaqillik ko'ch., 30-uy	4	71.784492	40.384138	\N	Yangi tarif rejasiga o'tish	Ombordan chiqarishga tayyor		t	in_warehouse	2025-09-24 13:01:01.15963+05	2025-09-24 17:01:01.15963+05
7	\N	1	Toshkent sh., Chilonzor t., 1-uy	1	69.240562	41.311081	5	Yangi ulanish kerak	JM tomonidan tasdiqlangan		t	in_warehouse	2025-09-24 14:09:30.472643+05	2025-09-24 17:09:30.472643+05
8	\N	2	Samarqand sh., Registon ko'ch., 5-uy	2	66.97559	39.627012	4	Internet tezligini oshirish	Texnik ko'rik kerak		t	in_warehouse	2025-09-24 14:39:30.472643+05	2025-09-24 17:09:30.472643+05
9	\N	3	Buxoro sh., Mustaqillik ko'ch., 25-uy	1	64.585262	39.767477	\N	Telefon liniyasini tiklash	\N		t	in_warehouse	2025-09-24 15:09:30.472643+05	2025-09-24 17:09:30.472643+05
10	\N	4	Andijon sh., Navoi ko'ch., 10-uy	3	72.344415	40.781731	3	Kabel almashtirish	Materiallar tayyor		t	in_warehouse	2025-09-24 15:39:30.472643+05	2025-09-24 17:09:30.472643+05
11	\N	5	Farg'ona sh., Mustaqillik ko'ch., 15-uy	2	71.784492	40.384138	\N	Modem sozlash	Tezkor bajarish kerak		t	in_warehouse	2025-09-24 16:09:30.472643+05	2025-09-24 17:09:30.472643+05
1	2	\N	Chilonzor 12-45	1	\N	\N	\N	\N	\N		t	between_controller_technician	2025-09-24 16:58:36.098947+05	2025-09-26 15:58:03.593418+05
13	11	andijon	15ariq	2	\N	\N	\N	\N	\N		t	completed	2025-09-26 15:36:51.131131+05	2025-09-26 16:06:35.507379+05
14	11	toshkent shahri	cholobod	2	64.674757	40.615796	\N	\N	\N		t	in_technician_work	2025-09-26 15:39:02.692428+05	2025-09-26 16:35:56.30705+05
12	11	navoiy	qorachol	2	\N	\N	\N	\N	\N		f	in_technician_work	2025-09-26 15:36:17.865382+05	2025-09-26 16:45:06.305527+05
\.


--
-- Data for Name: connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connections (id, sender_id, recipient_id, connection_order_id, technician_id, saff_id, created_at, updated_at, sender_status, recipient_status, connecion_id) FROM stdin;
1	4	10	13	\N	\N	2025-09-26 15:41:12.239321+05	2025-09-26 15:41:12.239321+05	in_manager	in_junior_manager	13
2	4	10	14	\N	\N	2025-09-26 15:41:20.633503+05	2025-09-26 15:41:20.633503+05	in_manager	in_junior_manager	14
3	10	8	13	\N	\N	2025-09-26 15:41:40.500772+05	2025-09-26 15:41:40.500772+05	in_junior_manager	in_controller	13
4	10	8	14	\N	\N	2025-09-26 15:41:44.672146+05	2025-09-26 15:41:44.672146+05	in_junior_manager	in_controller	14
5	4	10	12	\N	\N	2025-09-26 15:52:33.642618+05	2025-09-26 15:52:33.642618+05	in_manager	in_junior_manager	12
6	4	10	1	\N	\N	2025-09-26 15:52:40.394444+05	2025-09-26 15:52:40.394444+05	in_manager	in_junior_manager	1
7	10	8	12	\N	\N	2025-09-26 15:52:48.617418+05	2025-09-26 15:52:48.617418+05	in_junior_manager	in_controller	12
8	10	8	1	\N	\N	2025-09-26 15:52:52.126644+05	2025-09-26 15:52:52.126644+05	in_junior_manager	in_controller	1
9	9	8	14	\N	\N	2025-09-26 15:55:11.608719+05	2025-09-26 15:55:11.608719+05	in_controller	between_controller_technician	14
10	9	8	\N	12	\N	2025-09-26 15:56:46.913019+05	2025-09-26 15:56:46.913019+05	in_controller	between_controller_technician	\N
11	9	8	13	\N	\N	2025-09-26 15:57:13.01219+05	2025-09-26 15:57:13.01219+05	in_controller	between_controller_technician	13
12	9	8	12	\N	\N	2025-09-26 15:57:34.091281+05	2025-09-26 15:57:34.091281+05	in_controller	between_controller_technician	12
13	9	8	1	\N	\N	2025-09-26 15:58:03.593418+05	2025-09-26 15:58:03.593418+05	in_controller	between_controller_technician	1
14	9	8	\N	11	\N	2025-09-26 15:58:20.766646+05	2025-09-26 15:58:20.766646+05	in_controller	between_controller_technician	\N
15	9	8	\N	\N	12	2025-09-26 16:05:16.554507+05	2025-09-26 16:05:16.554507+05	in_controller	between_controller_technician	\N
16	9	8	\N	\N	11	2025-09-26 16:05:30.501233+05	2025-09-26 16:05:30.501233+05	in_controller	between_controller_technician	\N
17	8	8	13	\N	\N	2025-09-26 16:06:02.201411+05	2025-09-26 16:06:02.201411+05	between_controller_technician	in_technician	13
18	8	8	13	\N	\N	2025-09-26 16:06:06.931034+05	2025-09-26 16:06:06.931034+05	in_technician	in_technician_work	13
19	8	8	13	\N	\N	2025-09-26 16:06:35.507379+05	2025-09-26 16:06:35.507379+05	in_technician_work	completed	13
20	8	8	\N	12	\N	2025-09-26 16:16:40.345476+05	2025-09-26 16:16:40.345476+05	between_controller_technician	in_technician	\N
21	8	8	\N	11	\N	2025-09-26 16:16:47.170815+05	2025-09-26 16:16:47.170815+05	between_controller_technician	in_technician	\N
22	8	8	\N	11	\N	2025-09-26 16:16:58.448923+05	2025-09-26 16:16:58.448923+05	in_technician	in_technician_work	\N
23	8	8	\N	11	\N	2025-09-26 16:17:39.023234+05	2025-09-26 16:17:39.023234+05	in_technician_work	completed	\N
24	8	8	12	\N	\N	2025-09-26 16:26:12.861574+05	2025-09-26 16:26:12.861574+05	between_controller_technician	in_technician	12
25	8	8	12	\N	\N	2025-09-26 16:26:16.34416+05	2025-09-26 16:26:16.34416+05	in_technician	in_technician_work	12
26	8	8	14	\N	\N	2025-09-26 16:35:52.736135+05	2025-09-26 16:35:52.736135+05	between_controller_technician	in_technician	14
27	8	8	14	\N	\N	2025-09-26 16:35:56.30705+05	2025-09-26 16:35:56.30705+05	in_technician	in_technician_work	14
28	9	8	\N	\N	13	2025-09-26 16:45:32.083466+05	2025-09-26 16:45:32.083466+05	in_controller	between_controller_technician	\N
\.


--
-- Data for Name: material_and_technician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_and_technician (id, user_id, material_id, quantity) FROM stdin;
1	5	8	33
2	6	8	33
3	7	8	33
4	5	9	8
5	6	9	8
6	7	9	8
7	5	10	10
8	6	10	10
9	7	10	10
10	5	11	66
11	6	11	66
12	7	11	66
13	5	12	16
14	6	12	16
15	7	12	16
22	8	11	2
23	8	16	8
24	8	18	400
25	8	17	6
\.


--
-- Data for Name: material_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_requests (id, description, user_id, applications_id, material_id, connection_order_id, technician_order_id, saff_order_id, quantity, price, total_price) FROM stdin;
1	Test - Yangi ulanish uchun optik kabel	1	1	8	1	\N	\N	50	15.50	775.00
2	Test - Router ornatish uchun	1	2	9	2	\N	\N	1	85.00	85.00
3	Test - Ethernet kabel va konnektorlar	1	3	11	3	\N	\N	20	2.50	50.00
4	Test - Modem almashtirish uchun	1	4	10	\N	1	\N	1	45.00	45.00
5	Test - Splitter va konnektorlar	1	5	12	\N	2	\N	2	12.00	24.00
6	\N	8	13	11	\N	\N	\N	1	2.50	2.50
7	\N	8	11	11	\N	\N	\N	1	2.50	2.50
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, name, price, description, quantity, serial_number, created_at, updated_at) FROM stdin;
2	Кабель оптический	18000	\N	0	OPT-002	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
8	Test Optik kabel	15.50	Yuqori sifatli optik kabel	1	TEST-OPT-001	2025-09-24 17:37:22.512351+05	2025-09-26 14:49:12.665843+05
9	Test Router TP-Link	85.00	Wi-Fi router uy uchun	1	TEST-RTR-001	2025-09-24 17:37:22.512351+05	2025-09-26 14:49:12.665843+05
10	Test Modem ADSL	45.00	ADSL internet modemi	0	TEST-MDM-001	2025-09-24 17:37:22.512351+05	2025-09-26 14:49:12.665843+05
12	Test Splitter	12.00	Signal ajratuvchi	2	TEST-SPL-001	2025-09-24 17:37:22.512351+05	2025-09-26 14:49:12.665843+05
11	Test Ethernet kabel	2.50	Cat6 ethernet kabeli	0	TEST-ETH-001	2025-09-24 17:37:22.512351+05	2025-09-26 16:03:31.282225+05
13	Switch 16-port	250.00	Ofis uchun 16 portli switch	5	SW-016-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
14	Patch panel 24-port	120.00	Server xonasi uchun patch panel	3	PP-024-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
15	Wi-Fi Router ASUS	95.00	Yuqori tezlikdagi Wi-Fi router	4	RTR-ASUS-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
19	Optical Splitter 1x4	25.00	Optik signalni 4 ga ajratuvchi splitter	8	OS-1X4-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
20	Fiber Cleaver	150.00	Optik tolani kesuvchi maxsus asbob	2	FC-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
21	ADSL Splitter	5.00	Telefon va internet signalini ajratuvchi	15	ADSL-SPL-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
22	Crimping Tool	20.00	Ethernet ulagichlarni siquvchi asbob	6	CT-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:07:55.097721+05
16	Power Supply 12V	18.00	12 voltli quvvat manbai	2	PS-12V-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:08:15.988435+05
18	RJ-45 Connector	0.50	Ethernet uchun RJ-45 ulagich	100	RJ45-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:08:27.093368+05
17	Media Converter	45.00	Optikdan Ethernetga o‘tkazuvchi qurilma	1	MC-001	2025-09-26 16:07:55.097721+05	2025-09-26 16:08:42.724729+05
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (id, title, description, created_by, created_at, updated_at) FROM stdin;
1	Hisobot	\N	2	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
\.


--
-- Data for Name: saff_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.saff_orders (id, user_id, phone, region, abonent_id, tarif_id, address, description, status, type_of_zayavka, is_active, created_at, updated_at) FROM stdin;
1	\N	+998901234567	1	AB123456	1	Toshkent sh., Chilonzor t., 1-uy	Yangi ulanish uchun ariza	in_warehouse	connection	t	2025-09-24 15:01:01.16432+05	2025-09-24 17:01:01.16432+05
2	\N	+998901234568	2	AB123457	2	Samarqand sh., Registon ko'ch., 5-uy	Internet tezligini oshirish	in_warehouse	technician	t	2025-09-24 15:31:01.16432+05	2025-09-24 17:01:01.16432+05
3	\N	+998901234569	3	AB123458	1	Buxoro sh., Mustaqillik ko'ch., 25-uy	Telefon liniyasini tiklash	in_warehouse	technician	t	2025-09-24 16:16:01.16432+05	2025-09-24 17:01:01.16432+05
4	\N	+998901234570	4	AB123459	3	Andijon sh., Navoi ko'ch., 10-uy	Kabel almashtirish	in_warehouse	connection	t	2025-09-24 16:31:01.16432+05	2025-09-24 17:01:01.16432+05
5	\N	+998901234571	5	AB123460	2	Farg'ona sh., Mustaqillik ko'ch., 15-uy	Modem sozlash	in_warehouse	technician	t	2025-09-24 16:46:01.16432+05	2025-09-24 17:01:01.16432+05
6	\N	+998901234567	1	AB123456	1	Toshkent sh., Chilonzor t., 1-uy	Yangi ulanish uchun ariza	in_warehouse	connection	t	2025-09-24 15:09:30.481428+05	2025-09-24 17:09:30.481428+05
7	\N	+998901234568	2	AB123457	2	Samarqand sh., Registon ko'ch., 5-uy	Internet tezligini oshirish	in_warehouse	technician	t	2025-09-24 15:39:30.481428+05	2025-09-24 17:09:30.481428+05
8	\N	+998901234569	3	AB123458	1	Buxoro sh., Mustaqillik ko'ch., 25-uy	Telefon liniyasini tiklash	in_warehouse	technician	t	2025-09-24 16:24:30.481428+05	2025-09-24 17:09:30.481428+05
9	\N	+998901234570	4	AB123459	3	Andijon sh., Navoi ko'ch., 10-uy	Kabel almashtirish	in_warehouse	connection	t	2025-09-24 16:39:30.481428+05	2025-09-24 17:09:30.481428+05
10	\N	+998901234571	5	AB123460	2	Farg'ona sh., Mustaqillik ko'ch., 15-uy	Modem sozlash	in_warehouse	technician	t	2025-09-24 16:54:30.481428+05	2025-09-24 17:09:30.481428+05
12	4	998911223344	11	3	\N	fwefwefwqaf	geregaewsgrwesg	between_controller_technician	technician	t	2025-09-26 16:04:43.953813+05	2025-09-26 16:05:16.554507+05
11	4	998911223344	9	3	1	faesfawfawesfwes		between_controller_technician	connection	t	2025-09-26 16:04:12.981794+05	2025-09-26 16:05:30.501233+05
13	4	998911223344	5	3	3	qfqwfqwf		between_controller_technician	connection	t	2025-09-26 16:39:30.712567+05	2025-09-26 16:45:32.083466+05
\.


--
-- Data for Name: smart_service_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.smart_service_orders (id, user_id, category, service_type, address, longitude, latitude, is_active, created_at, updated_at) FROM stdin;
1	2	internet_tarmoq_xizmatlari	wi_fi_tarmoqlarini_ornatish_sozlash	Chilonzor	\N	\N	t	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
2	3	internet_tarmoq_xizmatlari	ustanovka_nastroyka_wi_fi_setey	ул. Пушкина	\N	\N	t	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
\.


--
-- Data for Name: tarif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarif (id, name, picture, created_at, updated_at) FROM stdin;
1	Hammasi birga 4		2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
2	Hammasi birga 3+		2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
3	Hammasi birga 3		2025-09-24 16:58:36.098947+05	2025-09-26 15:39:11.194001+05
4	Hammasi birga 2		2025-09-24 16:58:36.098947+05	2025-09-26 15:39:28.226541+05
\.


--
-- Data for Name: technician_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.technician_orders (id, user_id, region, abonent_id, address, media, longitude, latitude, description, description_ish, description_operator, status, rating, notes, is_active, created_at, updated_at) FROM stdin;
1	2	1	AB123456	Toshkent sh., Chilonzor t., 1-uy	\N	69.240562	41.311081	Internet aloqasi uzilmoqda	\N	\N	in_warehouse	\N	Diagnostika o'tkazildi, material kerak	t	2025-09-24 16:01:01.162374+05	2025-09-24 17:10:11.617079+05
2	3	2	AB123457	Samarqand sh., Registon ko'ch., 15-uy	\N	66.975681	39.627012	Televizor signali yo'q	\N	\N	in_warehouse	\N	Kabel almashtirish kerak	t	2025-09-22 17:01:01.162374+05	2025-09-24 17:10:11.625776+05
3	4	3	AB123458	Buxoro sh., Mustaqillik ko'ch., 25-uy	\N	64.585262	39.767477	Telefon aloqasi ishlamayapti	\N	\N	in_warehouse	\N	Yangi modem o'rnatish kerak	t	2025-09-24 12:01:01.162374+05	2025-09-24 17:10:11.627032+05
4	1	1	AB123459	Andijon sh., Navoi ko'ch., 10-uy	\N	72.344415	40.78237	Internet tezligi sekin	\N	\N	in_warehouse	\N	Router sozlash va yangilash	t	2025-09-24 16:16:01.162374+05	2025-09-24 17:11:08.845078+05
5	2	2	AB123460	Farg'ona sh., Mustaqillik ko'ch., 30-uy	\N	71.784492	40.384138	Barcha xizmatlar ishlamayapti	\N	\N	in_warehouse	\N	To'liq texnik ko'rik kerak	t	2025-09-24 11:01:01.162374+05	2025-09-24 17:11:08.85082+05
6	3	1	AB123456	Toshkent sh., Chilonzor t., 1-uy	\N	\N	\N	Internet aloqasi uzilmoqda	Kabel tekshirish va almashtirish	\N	in_warehouse	\N	Diagnostika o'tkazildi, material kerak	t	2025-09-24 14:24:30.480304+05	2025-09-24 17:11:08.851375+05
7	4	2	AB123457	Samarqand sh., Registon ko'ch., 5-uy	\N	\N	\N	TV signal sifati yomon	Antenna sozlash	\N	in_warehouse	\N	Yangi antenna kerak	t	2025-09-24 14:54:30.480304+05	2025-09-24 17:11:08.851893+05
8	1	3	AB123458	Buxoro sh., Mustaqillik ko'ch., 25-uy	\N	\N	\N	Telefon ishlamayapti	Liniya tiklash	\N	in_warehouse	\N	Kabel zararlanган	t	2025-09-24 15:24:30.480304+05	2025-09-24 17:11:08.852327+05
9	2	4	AB123459	Andijon sh., Navoi ko'ch., 10-uy	\N	\N	\N	Internet tezligi sekin	Modem almashtirish	\N	in_warehouse	\N	Yangi modem tayyor	t	2025-09-24 15:54:30.480304+05	2025-09-24 17:11:08.852774+05
10	3	5	AB123460	Farg'ona sh., Mustaqillik ko'ch., 15-uy	\N	\N	\N	Barcha xizmatlar ishlamayapti	To'liq texnik ko'rik kerak	\N	in_warehouse	\N	Kompleks ta'mirlash	t	2025-09-24 16:24:30.480304+05	2025-09-24 17:11:08.853159+05
12	11	6	65161661616	hayot kochai	AgACAgIAAxkBAAITMmjWbj6aFkgwTJjasfeQTBQodm1KAAKu9DEbPYe5Snt9-BiEXpeZAQADAgADeQADNgQ	64.494987	41.502636	hayot toxtab qoldi	\N	\N	in_technician	\N	\N	t	2025-09-26 15:43:30.218794+05	2025-09-26 16:16:40.345476+05
13	11	1	12345678	Abdulla Qodiriy ko'chasi, 1-uy	\N	\N	\N	Bakirali meshat qilyapti	\N	\N	in_controller	\N	\N	t	2025-09-26 16:17:02.776135+05	2025-09-26 16:17:02.776135+05
11	11	6	1234567890	manzil kocha	AgACAgIAAxkBAAITBmjWbZwwy46InOmj_0rgr6wm4QnMAAKo9DEbPYe5Sp-mDKL9mvgNAQADAgADeQADNgQ	\N	\N	wifi router portlab ketdi	lkfajsdlfj asdjasdfl ajsdl asdfasd	\N	completed	\N	\N	t	2025-09-26 15:40:37.505731+05	2025-09-26 16:17:39.023234+05
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked, created_at, updated_at) FROM stdin;
2	210000001	Aziz Karimov	aziz_k	998901234567	uz	1	Chilonzor	client	1001	f	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
3	310000001	Александр Петров	alex_petrov	998911223344	ru	1	ул. Пушкина	client	2001	f	2025-09-24 16:58:36.098947+05	2025-09-24 16:58:36.098947+05
5	910000001	Ali Rahimov	tech_ali	998901110011	uz	1	Toshkent	technician	\N	f	2025-09-26 14:49:12.665843+05	2025-09-26 14:49:12.665843+05
6	910000002	Bekzod Karimov	tech_bek	998901110022	uz	1	Toshkent	technician	\N	f	2025-09-26 14:49:12.665843+05	2025-09-26 14:49:12.665843+05
7	910000003	Sardor Akmalov	tech_sardor	998901110033	uz	1	Toshkent	technician	\N	f	2025-09-26 14:49:12.665843+05	2025-09-26 14:49:12.665843+05
10	5955605892	Salom	gulsara_yakubjanova	998908103399	uz	\N	\N	junior_manager	\N	f	2025-09-26 15:31:00.778945+05	2025-09-26 15:33:40.249929+05
1	1978574076	Ulug‘bek Administrator	ulugbekbb	998900042544	uz	1	Toshkent	warehouse	ADM001	f	2025-09-24 16:58:36.098947+05	2025-09-26 15:34:10.954112+05
11	8401544590	Abdumuratov Abdumannop	abdumuratov_off	+998912340024	uz	\N	\N	client	\N	f	2025-09-26 15:35:18.802427+05	2025-09-26 16:15:28.575195+05
4	8188731606	Ibrohimbek	ibrohim_fx01	+998881249327	uz	\N	\N	manager	\N	f	2025-09-24 16:58:44.697161+05	2025-09-26 16:39:30.60686+05
9	7793341014	alijon	bakiralizokirov	+998937490211	uz	\N	\N	callcenter_supervisor	\N	f	2025-09-26 15:30:37.514558+05	2025-09-26 16:56:44.323535+05
8	2129817198	Bakirali Zokirov	bakirali_zokirov	+998908200120	uz	\N	\N	callcenter_operator	\N	f	2025-09-26 15:27:39.231117+05	2025-09-26 17:00:32.08924+05
\.


--
-- Name: akt_documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_documents_id_seq', 3, true);


--
-- Name: akt_ratings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.akt_ratings_id_seq', 3, true);


--
-- Name: connection_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connection_orders_id_seq', 14, true);


--
-- Name: connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.connections_id_seq', 28, true);


--
-- Name: material_and_technician_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_and_technician_id_seq', 25, true);


--
-- Name: material_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.material_requests_id_seq', 7, true);


--
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_seq', 48, true);


--
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_id_seq', 1, true);


--
-- Name: saff_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saff_orders_id_seq', 13, true);


--
-- Name: smart_service_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.smart_service_orders_id_seq', 2, true);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 4, true);


--
-- Name: technician_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.technician_orders_id_seq', 13, true);


--
-- Name: user_sequential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sequential_id_seq', 11, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: akt_documents akt_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_documents
    ADD CONSTRAINT akt_documents_pkey PRIMARY KEY (id);


--
-- Name: akt_ratings akt_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.akt_ratings
    ADD CONSTRAINT akt_ratings_pkey PRIMARY KEY (id);


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
-- Name: akt_documents_request_id_request_type_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX akt_documents_request_id_request_type_key ON public.akt_documents USING btree (request_id, request_type);


--
-- Name: akt_ratings_request_id_request_type_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX akt_ratings_request_id_request_type_key ON public.akt_ratings USING btree (request_id, request_type);


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
-- Name: idx_connection_orders_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connection_orders_created ON public.connection_orders USING btree (created_at);


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
-- Name: idx_connections_technician_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connections_technician_id ON public.connections USING btree (technician_id);


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

CREATE INDEX idx_saff_ccs_active_created ON public.saff_orders USING btree (created_at, id) WHERE ((status = 'in_call_center'::public.saff_order_status) AND (is_active = true));


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
-- Name: idx_technician_orders_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_technician_orders_created ON public.technician_orders USING btree (created_at);


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
-- Name: idx_users_role; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_role ON public.users USING btree (role);


--
-- Name: ux_mat_tech_user_material; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ux_mat_tech_user_material ON public.material_and_technician USING btree (user_id, material_id);


--
-- Name: ux_material_requests_triplet; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ux_material_requests_triplet ON public.material_requests USING btree (user_id, applications_id, material_id);


--
-- Name: connection_orders trg_connection_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_connection_orders_updated_at BEFORE UPDATE ON public.connection_orders FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: connections trg_connections_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_connections_updated_at BEFORE UPDATE ON public.connections FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: materials trg_materials_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_materials_updated_at BEFORE UPDATE ON public.materials FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: smart_service_orders trg_normalize_sso_category_bi; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_normalize_sso_category_bi BEFORE INSERT ON public.smart_service_orders FOR EACH ROW EXECUTE FUNCTION public.trg_normalize_sso_category();


--
-- Name: reports trg_reports_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_reports_updated_at BEFORE UPDATE ON public.reports FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: saff_orders trg_saff_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_saff_orders_updated_at BEFORE UPDATE ON public.saff_orders FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: smart_service_orders trg_sso_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_sso_updated_at BEFORE UPDATE ON public.smart_service_orders FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: connections trg_sync_connections_ids_bi; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_sync_connections_ids_bi BEFORE INSERT OR UPDATE ON public.connections FOR EACH ROW EXECUTE FUNCTION public.trg_sync_connections_ids();


--
-- Name: tarif trg_tarif_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_tarif_updated_at BEFORE UPDATE ON public.tarif FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: technician_orders trg_technician_orders_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_technician_orders_updated_at BEFORE UPDATE ON public.technician_orders FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users trg_users_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


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
-- Name: connections connections_connection_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_connection_order_id_fkey FOREIGN KEY (connection_order_id) REFERENCES public.connection_orders(id) ON DELETE SET NULL;


--
-- Name: connections connections_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_saff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_saff_id_fkey FOREIGN KEY (saff_id) REFERENCES public.saff_orders(id) ON DELETE SET NULL;


--
-- Name: connections connections_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: connections connections_technician_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_technician_id_fkey FOREIGN KEY (technician_id) REFERENCES public.technician_orders(id) ON DELETE SET NULL;


--
-- Name: material_and_technician material_and_technician_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT material_and_technician_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.materials(id) ON DELETE CASCADE;


--
-- Name: material_and_technician material_and_technician_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_and_technician
    ADD CONSTRAINT material_and_technician_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: material_requests material_requests_connection_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_connection_order_id_fkey FOREIGN KEY (connection_order_id) REFERENCES public.connection_orders(id) ON DELETE SET NULL;


--
-- Name: material_requests material_requests_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.materials(id) ON DELETE CASCADE;


--
-- Name: material_requests material_requests_saff_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_saff_order_id_fkey FOREIGN KEY (saff_order_id) REFERENCES public.saff_orders(id) ON DELETE SET NULL;


--
-- Name: material_requests material_requests_technician_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_technician_order_id_fkey FOREIGN KEY (technician_order_id) REFERENCES public.technician_orders(id) ON DELETE SET NULL;


--
-- Name: material_requests material_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_requests
    ADD CONSTRAINT material_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reports reports_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id) ON DELETE SET NULL;


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

