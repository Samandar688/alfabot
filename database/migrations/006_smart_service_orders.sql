-- SmartService orders table
CREATE TYPE smart_service_category AS ENUM (
  'aqlli_avtomatlashtirilgan_xizmatlar',
  'xavfsizlik_kuzatuv_tizimlari', 
  'internet_tarmoq_xizmatlari',
  'energiya_yashil_texnologiyalar',
  'multimediya_aloqa_tizimlari',
  'maxsus_qoshimcha_xizmatlar'
);

CREATE TYPE smart_service_type AS ENUM (
  -- Aqlli uv va avtomatlashtirilgan xizmatlar (1-8)
  'aqlli_uy_tizimlarini_ornatish_sozlash',
  'aqlli_yoritish_smart_lighting_tizimlari', 
  'aqlli_termostat_iqlim_nazarati_tizimlari',
  'smart_lock_internet_orqali_boshqariladigan_eshik_qulfi_tizimlari',
  'aqlli_rozetalar_energiya_monitoring_tizimlari',
  'uyni_masofadan_boshqarish_qurilmalari_yagona_uzim_orqali_boshqarish',
  'aqlli_pardalari_jaluz_tizimlari',
  'aqlli_malahiy_texnika_integratsiyasi',
  
  -- Xavfsizlik va kuzatuv tizimlari (9-16)
  'videokuzatuv_kameralarini_ornatish_ip_va_analog',
  'kamera_arxiv_tizimlari_bulutli_saqlash_xizmatlari',
  'domofon_tizimlari_ornatish',
  'xavfsizlik_signalizatsiyasi_harakat_sensorlarini_ornatish',
  'yong_signalizatsiyasi_tizimlari',
  'gaz_sizish_sav_toshqinliqqa_qarshi_tizimlar',
  'yuzni_tanish_face_recognition_tizimlari',
  'avtomatik_eshik_darvoza_boshqaruv_tizimlari',
  
  -- Internet va tarmoq xizmatlari (17-24)
  'wi_fi_tarmoqlarini_ornatish_sozlash',
  'wi_fi_qamrov_zonasini_kengaytirish_access_point',
  'mobil_aloqa_signalini_kuchaytirish_repeater',
  'ofis_va_uy_uchun_lokal_tarmoq_lan_qurish',
  'internet_provayder_xizmatlarini_ulash',
  'server_va_nas_qurilmalarini_ornatish',
  'bulutli_fayl_almashish_zaxira_tizimlari',
  'vpn_va_xavfsiz_internet_ulanishlarini_tashkil_qilish',
  
  -- Energiya va yashil texnologiyalar (25-29)
  'quyosh_panellarini_ornatish_ulash',
  'quyosh_batareyalari_orqali_energiya_saqlash_tizimlari',
  'shamol_generatorlarini_ornatish',
  'elektr_energiyasini_tejovchi_yoritish_tizimlari',
  'avtomatik_suv_orish_tizimlari_smart_irrigation',
  
  -- Multimediya va aloqa tizimlari (30-35)
  'smart_tv_ornatish_ulash',
  'uy_kinoteatri_tizimlari_ornatish',
  'audio_tizimlar_multiroom',
  'ip_telefoniya_mini_ats_tizimlarini_tashkil_qilish',
  'video_konferensiya_tizimlari',
  'interaktiv_taqdimot_tizimlari_proyektor_led_ekran',
  
  -- Maxsus va qo'shimcha xizmatlar (36-42)
  'aqlli_ofis_tizimlarini_ornatish',
  'data_markaz_server_room_loyihalash_montaj_qilish',
  'qurilma_tizimlar_uchun_texnik_xizmat_korsatish',
  'dasturiy_taminotni_ornatish_yangilash',
  'iot_internet_of_things_qurilmalarini_integratsiya_qilish',
  'qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash',
  'suniy_intellekt_asosidagi_uy_ofis_boshqaruv_tizimlari'
);

CREATE TABLE IF NOT EXISTS smart_service_orders (
  id           BIGSERIAL PRIMARY KEY,
  user_id      BIGINT REFERENCES users(id) ON DELETE SET NULL,
  category     smart_service_category NOT NULL,
  service_type smart_service_type NOT NULL,
  address      TEXT NOT NULL,
  longitude    DOUBLE PRECISION,
  latitude     DOUBLE PRECISION,
  is_active    BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_smart_service_orders_user ON smart_service_orders(user_id);
CREATE INDEX idx_smart_service_orders_category ON smart_service_orders(category);
CREATE INDEX idx_smart_service_orders_created ON smart_service_orders(created_at);
CREATE INDEX IF NOT EXISTS idx_sso_created_at ON smart_service_orders (created_at DESC);

-- Trigger for updated_at
CREATE TRIGGER smart_service_orders_updated_at
  BEFORE UPDATE ON smart_service_orders
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

  