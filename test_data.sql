-- ALFABOT TEST DATA SQL FILE
-- Generated for testing export functionality and other features
-- Execute this file to populate the database with sample data

-- Clear existing data (optional - uncomment if needed)
-- TRUNCATE TABLE akt_documents, akt_ratings, connections, material_and_technician, material_requests, reports CASCADE;
-- TRUNCATE TABLE connection_orders, technician_orders, saff_orders, smart_service_orders CASCADE;
-- TRUNCATE TABLE materials, tarif, users CASCADE;


-- ============================================================================
-- 2. USERS TABLE - Different roles for testing
-- ============================================================================
INSERT INTO users (id, telegram_id, full_name, username, phone, language, region, address, role, abonent_id, is_blocked, created_at, updated_at) VALUES
-- Admin users
(1, 111111111, 'Admin Adminov', 'admin_user', '+998901234567', 'uz', 1, 'Toshkent, Chilonzor tumani', 'admin', 'ADM001', false, NOW(), NOW()),
(2, 222222222, 'Админ Админов', 'admin_ru', '+998901234568', 'ru', 1, 'Ташкент, Чиланзарский район', 'admin', 'ADM002', false, NOW(), NOW()),

-- Manager users
(3, 333333333, 'Manager Managerov', 'manager_user', '+998901234569', 'uz', 1, 'Toshkent, Yunusobod tumani', 'manager', 'MNG001', false, NOW(), NOW()),
(4, 444444444, 'Менеджер Менеджеров', 'manager_ru', '+998901234570', 'ru', 2, 'Самарканд, центральный район', 'manager', 'MNG002', false, NOW(), NOW()),

-- Junior Manager users
(5, 555555555, 'Junior Manager Juniorov', 'jm_user', '+998901234571', 'uz', 1, 'Toshkent, Mirzo Ulugbek tumani', 'junior_manager', 'JMG001', false, NOW(), NOW()),

-- Technician users
(6, 666666666, 'Technician Technicov', 'tech_user', '+998901234572', 'uz', 1, 'Toshkent, Shayxontohur tumani', 'technician', 'TCH001', false, NOW(), NOW()),
(7, 777777777, 'Техник Техников', 'tech_ru', '+998901234573', 'ru', 2, 'Самарканд, Сиабский район', 'technician', 'TCH002', false, NOW(), NOW()),
(8, 888888888, 'Technician Warehouse', 'tech_warehouse', '+998901234574', 'uz', 3, 'Buxoro, Markaz tumani', 'technician', 'TCH003', false, NOW(), NOW()),

-- Warehouse users
(9, 999999999, 'Warehouse Manager', 'warehouse_user', '+998901234575', 'uz', 1, 'Toshkent, Sergeli tumani', 'warehouse', 'WRH001', false, NOW(), NOW()),
(10, 1010101010, 'Склад Менеджер', 'warehouse_ru', '+998901234576', 'ru', 1, 'Ташкент, Сергелийский район', 'warehouse', 'WRH002', false, NOW(), NOW()),

-- Call Center users
(11, 1111111111, 'Call Center Operator', 'call_center_operator', '+998901234577', 'uz', 1, 'Toshkent, Olmazor tumani', 'callcenter_operator', 'CCO001', false, NOW(), NOW()),
(12, 1212121212, 'Call Center Supervisor', 'callcenter_supervisor', '+998901234578', 'uz', 1, 'Toshkent, Bektemir tumani', 'callcenter_supervisor', 'CCS001', false, NOW(), NOW()),

-- Controller users
(13, 1313131313, 'Controller User', 'controller_user', '+998901234579', 'uz', 1, 'Toshkent, Yashnobod tumani', 'controller', 'CTR001', false, NOW(), NOW()),

-- Client users
(14, 1414141414, 'Client Clientov', 'client_user', '+998901234580', 'uz', 1, 'Toshkent, Hamza tumani, 15-uy', 'client', 'CLT001', false, NOW(), NOW()),
(15, 1515151515, 'Клиент Клиентов', 'client_ru', '+998901234581', 'ru', 2, 'Самарканд, ул. Регистан, 25', 'client', 'CLT002', false, NOW(), NOW()),
(16, 1616161616, 'Client Test User', 'client_test', '+998901234582', 'uz', 3, 'Buxoro, Kogon tumani, 8-uy', 'client', 'CLT003', false, NOW(), NOW()),
(17, 1717171717, 'Client Premium', 'client_premium', '+998901234583', 'uz', 1, 'Toshkent, Mirobod tumani, 45-uy', 'client', 'CLT004', false, NOW(), NOW()),
(18, 1818181818, 'Client Business', 'client_business', '+998901234584', 'ru', 4, 'Наманган, центральный район, 12', 'client', 'CLT005', false, NOW(), NOW()),

-- Additional clients for more comprehensive testing
(19, 1919191919, 'Client VIP', 'client_vip', '+998901234585', 'uz', 1, 'Toshkent, Yunusobod tumani, 88-uy', 'client', 'CLT006', false, NOW(), NOW()),
(20, 2020202020, 'Client Corporate', 'client_corp', '+998901234586', 'ru', 2, 'Самарканд, ул. Амира Темура, 15', 'client', 'CLT007', false, NOW(), NOW()),
(21, 2121212121, 'Client Standard', 'client_std', '+998901234587', 'uz', 3, 'Buxoro, Shofirkon tumani, 22-uy', 'client', 'CLT008', false, NOW(), NOW()),
(22, 2222222222, 'Client Economy', 'client_eco', '+998901234588', 'uz', 4, 'Namangan, Pop tumani, 33-uy', 'client', 'CLT009', false, NOW(), NOW()),
(23, 2323232323, 'Client Enterprise', 'client_ent', '+998901234589', 'ru', 5, 'Андижан, центральный район, 44', 'client', 'CLT010', false, NOW(), NOW());

-- ============================================================================
-- 3. MATERIALS TABLE - Warehouse inventory items
-- ============================================================================
-- Clear existing data first to avoid conflicts
-- Delete referencing records first to avoid foreign key constraint violations


INSERT INTO materials (name, price, description, quantity, serial_number, created_at, updated_at) VALUES
-- Network equipment
('Router TP-Link Archer C6', 350000, 'Wi-Fi router 1200 Mbps, 4 antenna', 25, 'RTR-001-2024', NOW(), NOW()),
('Modem ADSL ZTE', 180000, 'ADSL modem for internet connection', 15, 'MDM-002-2024', NOW(), NOW()),
('Switch 8-port Gigabit', 420000, '8-port Gigabit Ethernet switch', 12, 'SWT-003-2024', NOW(), NOW()),
('ONT Huawei HG8245H', 280000, 'Optical Network Terminal GPON', 30, 'ONT-004-2024', NOW(), NOW()),
('Wi-Fi Extender', 150000, 'Wi-Fi signal extender/repeater', 8, 'EXT-005-2024', NOW(), NOW()),

-- Cables and connectors
('UTP Cable Cat6 (100m)', 85000, 'Category 6 UTP cable roll 100 meters', 50, 'CBL-006-2024', NOW(), NOW()),
('Fiber Optic Cable (1km)', 1200000, 'Single mode fiber optic cable 1km', 5, 'FOC-007-2024', NOW(), NOW()),
('RJ45 Connector (100pcs)', 25000, 'RJ45 connectors pack of 100 pieces', 20, 'RJ45-008-2024', NOW(), NOW()),
('Coaxial Cable RG6 (100m)', 95000, 'RG6 coaxial cable for TV/Internet', 18, 'COX-009-2024', NOW(), NOW()),

-- Installation tools and accessories
('Crimping Tool RJ45', 65000, 'Professional RJ45 crimping tool', 6, 'CRM-010-2024', NOW(), NOW()),
('Cable Tester', 120000, 'Network cable tester for UTP/STP', 4, 'TST-011-2024', NOW(), NOW()),
('Drill Bits Set', 45000, 'Set of drill bits for installation', 10, 'DRL-012-2024', NOW(), NOW()),
('Wall Mount Bracket', 35000, 'Universal wall mount for equipment', 22, 'MNT-013-2024', NOW(), NOW()),

-- Low stock items (for testing low stock functionality)
('Splitter 1:8', 75000, '1 to 8 optical splitter', 3, 'SPL-014-2024', NOW(), NOW()),
('Patch Cord 3m', 15000, '3 meter patch cord cable', 2, 'PCH-015-2024', NOW(), NOW()),

-- Out of stock items (for testing out of stock functionality)
('Media Converter', 250000, 'Fiber to Ethernet media converter', 0, 'MCV-016-2024', NOW(), NOW()),
('Optical Attenuator', 180000, 'Variable optical attenuator', 0, 'ATT-017-2024', NOW(), NOW()),

-- Additional materials for comprehensive testing
('Fiber Optik Kabel 100m', 2500000, 'Yuqori sifatli fiber optik kabel 100m', 15, 'FOK-018-2024', NOW(), NOW()),
('Network Switch 24-port', 1500000, '24 portli tarmoq kommutatori', 8, 'NSW-019-2024', NOW(), NOW()),
('WiFi Router AC1200', 450000, 'Simsiz internet routeri AC1200', 12, 'WFR-020-2024', NOW(), NOW()),
('Ethernet Cable Cat6 50m', 180000, 'Cat6 ethernet kabeli 50m', 20, 'ETC-021-2024', NOW(), NOW()),
('Power Adapter 12V 2A', 80000, 'Quvvat adaptori 12V 2A', 30, 'PWA-022-2024', NOW(), NOW()),
('Antenna Yagi 15dBi', 350000, 'Yonaltirilgan antenna 15dBi', 6, 'ANT-023-2024', NOW(), NOW()),
('Coaxial Cable RG6 100m', 220000, 'Koaksial kabel RG6 100m', 14, 'COX-024-2024', NOW(), NOW()),
('Signal Amplifier 20dB', 650000, 'Signal kuchaytirgichi 20dB', 4, 'SIG-025-2024', NOW(), NOW()),

-- Low stock materials for testing (quantity <= 10 but > 0)
('Test Low Stock Item 1', 100000, 'Past qoldiq test mahsuloti 1', 5, 'TLS-026-2024', NOW(), NOW()),
('Test Low Stock Item 2', 150000, 'Past qoldiq test mahsuloti 2', 3, 'TLS-027-2024', NOW(), NOW()),
('Test Low Stock Item 3', 200000, 'Past qoldiq test mahsuloti 3', 8, 'TLS-028-2024', NOW(), NOW()),

-- Out of stock materials for testing (quantity = 0)
('Test Out of Stock Item 1', 250000, 'Tugagan test mahsuloti 1', 0, 'TOS-029-2024', NOW(), NOW()),
('Test Out of Stock Item 2', 300000, 'Tugagan test mahsuloti 2', 0, 'TOS-030-2024', NOW(), NOW());

-- ============================================================================
-- 4. CONNECTION ORDERS TABLE - Various connection requests
-- ============================================================================
INSERT INTO connection_orders (id, user_id, region, address, tarif_id, longitude, latitude, rating, notes, jm_notes, is_active, status, created_at, updated_at, controller_notes) VALUES
(1, 14, 'Toshkent', 'Chilonzor tumani, 12-mavze, 15-uy', 1, 69.2401, 41.2995, NULL, 'Yangi ulanish', 'Mijoz bilan boglanildi', true, 'pending', NOW() - INTERVAL '2 days', NOW(), ''),
(2, 15, 'Samarqand', 'Registon kochasi 25-uy', 2, 66.9597, 39.6270, 5, 'Biznes ulanish', 'Texnik korik otkazildi', true, 'in_progress', NOW() - INTERVAL '1 day', NOW(), 'Texnik ishlar boshlandi'),
(3, 16, 'Buxoro', 'Kogon tumani, 8-uy', 3, 64.4211, 39.7747, NULL, 'Premium tarif', '', true, 'completed', NOW() - INTERVAL '5 days', NOW() - INTERVAL '1 day', 'Muvaffaqiyatli ulandi'),
(4, 17, 'Toshkent', 'Mirobod tumani, 45-uy', 4, 69.2785, 41.3111, 4, 'Ekonom tarif', 'Qoshimcha malumot kerak', true, 'pending', NOW() - INTERVAL '3 days', NOW(), ''),
(5, 18, 'Namangan', 'Markaz tumani, 12-uy', 1, 71.6726, 40.9983, NULL, 'Smart TV bilan', '', true, 'cancelled', NOW() - INTERVAL '7 days', NOW() - INTERVAL '2 days', 'Mijoz bekor qildi'),

-- Additional connection orders for comprehensive testing
(6, 19, 'Toshkent', 'Yunusobod tumani, 88-uy', 1, 69.2401, 41.2995, NULL, 'VIP ulanish - jarayonda', 'Maxsus mijoz', true, 'in_progress', NOW() - INTERVAL '1 day', NOW(), 'Texnik ishlar boshlandi'),
(7, 20, 'Samarqand', 'Amira Temura kochasi, 15-uy', 2, 66.9597, 39.6270, NULL, 'Корпоративное подключение - завершено', 'Korporativ mijoz', true, 'completed', NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day', 'Muvaffaqiyatli ulandi'),
(8, 21, 'Buxoro', 'Shofirkon tumani, 22-uy', 3, 64.4211, 39.7747, NULL, 'Standart ulanish - kutilmoqda', '', true, 'new', NOW() - INTERVAL '2 hours', NOW(), ''),
(9, 22, 'Namangan', 'Pop tumani, 33-uy', 4, 71.6726, 40.9983, NULL, 'Economy ulanish - bajarilmoqda', 'Oddiy mijoz', true, 'in_progress', NOW() - INTERVAL '4 hours', NOW(), 'Texnik tayinlandi'),
(10, 23, 'Andijon', 'Markaz tumani, 44-uy', 2, 70.9428, 40.7821, NULL, 'Enterprise подключение - готово', 'Korxona mijozi', true, 'completed', NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days', 'Muvaffaqiyatli ulandi');

-- ============================================================================
-- 5. TECHNICIAN ORDERS TABLE - Technical service requests
-- ============================================================================
INSERT INTO technician_orders (id, user_id, region, abonent_id, address, media, longitude, latitude, description, status, rating, notes, is_active, created_at, updated_at, description_ish) VALUES
(1, 14, 1, 'CLT001', 'Chilonzor tumani, 12-mavze, 15-uy', NULL, 69.2401, 41.2995, 'Internet tezligi sekin', 'new', NULL, '', true, NOW() - INTERVAL '1 day', NOW(), NULL),
(2, 15, 2, 'CLT002', 'Registon kochasi, 25-uy', 'problem_photo.jpg', 66.9597, 39.6270, 'Wi-Fi ishlamayapti', 'in_progress', NULL, 'Texnik yolda', true, NOW() - INTERVAL '2 hours', NOW(), NULL),
(3, 16, 3, 'CLT003', 'Kogon tumani, 8-uy', NULL, 64.4211, 39.7747, 'Kabel shikastlangan', 'completed', 5, 'Muammo hal qilindi', false, NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day', 'Yangi kabel ornatildi'),
(4, 17, 1, 'CLT004', 'Mirobod tumani, 45-uy', 'router_issue.jpg', 69.2785, 41.3111, 'Router qayta ishga tushmayapti', 'assigned', NULL, 'Texnik tayinlandi', true, NOW() - INTERVAL '4 hours', NOW(), NULL),
(5, 18, 4, 'CLT005', 'Markaz tumani, 12-uy', NULL, 71.6726, 40.9983, 'TV kanallari korinmayapti', 'new', NULL, '', true, NOW() - INTERVAL '6 hours', NOW(), NULL),

-- Additional technician orders for controller testing
(6, 19, 1, 'CLT006', 'Yunusobod tumani, 88-uy', NULL, 69.2401, 41.2995, 'Fiber optik kabel ornatish - VIP mijoz', 'new', NULL, 'Maxsus ehtiyot choralarini koring', true, NOW() - INTERVAL '2 hours', NOW(), NULL),
(7, 20, 2, 'CLT007', 'Amira Temura kochasi, 15-uy', NULL, 66.9597, 39.6270, 'Network switch sozlash - korporativ', 'in_progress', NULL, 'Konfiguratsiya faylini tayyorlang', true, NOW() - INTERVAL '1 day', NOW(), NULL),
(8, 21, 3, 'CLT008', 'Shofirkon tumani, 22-uy', NULL, 64.4211, 39.7747, 'WiFi router ornatish - standart', 'completed', 4, 'Muvaffaqiyatli ornatildi', false, NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day', 'Router sozlandi va test qilindi'),
(9, 22, 4, 'CLT009', 'Pop tumani, 33-uy', NULL, 71.6726, 40.9983, 'Ethernet kabel tortish - bekor qilindi', 'cancelled', NULL, 'Mijoz bekor qildi', false, NOW() - INTERVAL '2 days', NOW(), NULL),
(10, 23, 5, 'CLT010', 'Markaz tumani, 44-uy', NULL, 70.9428, 40.7821, 'Power adapter almashtirish - biznes', 'new', NULL, 'Eski adaptorni olib keling', true, NOW() - INTERVAL '4 hours', NOW(), NULL);

-- ============================================================================
-- 6. SAFF ORDERS TABLE - Staff orders
-- ============================================================================
INSERT INTO saff_orders (id, user_id, phone, region, abonent_id, tarif_id, address, description, status, type_of_zayavka, is_active, created_at, updated_at) VALUES
(1, 14, '+998901234580', 1, 'CLT001', 1, 'Chilonzor tumani, 12-mavze, 15-uy', 'Yangi ulanish sorovi', 'in_call_center', 'connection', true, NOW() - INTERVAL '2 days', NOW()),
(2, 15, '+998901234581', 2, 'CLT002', 2, 'Registon kochasi, 25-uy', 'Tarif ozgartirish', 'in_call_center', 'technician', true, NOW() - INTERVAL '1 day', NOW()),
(3, 16, '+998901234582', 3, 'CLT003', 3, 'Kogon tumani, 8-uy', 'Texnik yordam', 'completed', 'technician', false, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days'),
(4, 17, '+998901234583', 1, 'CLT004', 4, 'Mirobod tumani, 45-uy', 'Internet tezligini oshirish', 'in_manager', 'connection', true, NOW() - INTERVAL '3 hours', NOW()),
(5, 18, '+998901234584', 4, 'CLT005', 1, 'Markaz tumani, 12-uy', 'Qoshimcha xizmat', 'in_call_center', 'technician', true, NOW() - INTERVAL '1 hour', NOW());

-- ============================================================================
-- 7. SMART SERVICE ORDERS TABLE - Smart service requests
-- ============================================================================
INSERT INTO smart_service_orders (id, user_id, category, service_type, address, longitude, latitude, is_active, created_at, updated_at) VALUES
(1, 14, 'aqlli_avtomatlashtirilgan_xizmatlar', 'Fiber Internet Installation', 'Chilonzor tumani, 12-mavze, 15-uy', 69.2401, 41.2995, true, NOW() - INTERVAL '1 day', NOW()),
(2, 15, 'xavfsizlik_kuzatuv_tizimlari', 'Smart TV Setup', 'Registon kochasi, 25-uy', 66.9597, 39.6270, true, NOW() - INTERVAL '3 hours', NOW()),
(3, 16, 'internet_tarmoq_xizmatlari', 'VoIP Phone Installation', 'Kogon tumani, 8-uy', 64.4211, 39.7747, false, NOW() - INTERVAL '7 days', NOW() - INTERVAL '3 days'),
(4, 17, 'aqlli_avtomatlashtirilgan_xizmatlar', 'Wi-Fi Network Setup', 'Mirobod tumani, 45-uy', 69.2785, 41.3111, true, NOW() - INTERVAL '2 hours', NOW()),
(5, 18, 'xavfsizlik_kuzatuv_tizimlari', 'IPTV Configuration', 'Markaz tumani, 12-uy', 71.6726, 40.9983, true, NOW() - INTERVAL '30 minutes', NOW()),

-- Additional smart service orders for controller testing
(6, 19, 'aqlli_avtomatlashtirilgan_xizmatlar', 'Smart TV sozlash - VIP mijoz', 'Yunusobod tumani, 88-uy', 69.2401, 41.2995, true, NOW() - INTERVAL '2 hours', NOW()),
(7, 20, 'xavfsizlik_kuzatuv_tizimlari', 'Smart Home tizimi - korporativ', 'Amira Temura kochasi, 15-uy', 66.9597, 39.6270, true, NOW() - INTERVAL '1 day', NOW()),
(8, 21, 'internet_tarmoq_xizmatlari', 'Smart WiFi sozlash - standart', 'Shofirkon tumani, 22-uy', 64.4211, 39.7747, false, NOW() - INTERVAL '3 days', NOW() - INTERVAL '1 day'),
(9, 22, 'aqlli_avtomatlashtirilgan_xizmatlar', 'Smart Security - bekor qilindi', 'Pop tumani, 33-uy', 71.6726, 40.9983, false, NOW() - INTERVAL '2 days', NOW()),
(10, 23, 'xavfsizlik_kuzatuv_tizimlari', 'Smart Monitoring - biznes', 'Markaz tumani, 44-uy', 70.9428, 40.7821, true, NOW() - INTERVAL '4 hours', NOW());

-- ============================================================================
-- 8. MATERIAL_AND_TECHNICIAN TABLE - Materials assigned to technicians
-- ============================================================================
INSERT INTO material_and_technician (id, user_id, material_id, quantity) VALUES
(1, 6, 1, 3),  -- Technician 1 has 3 routers
(2, 6, 4, 5),  -- Technician 1 has 5 ONTs
(3, 6, 8, 10), -- Technician 1 has 10 RJ45 connectors
(4, 7, 2, 2),  -- Technician 2 has 2 modems
(5, 7, 6, 1),  -- Technician 2 has 1 UTP cable roll
(6, 7, 13, 4), -- Technician 2 has 4 wall mount brackets
(7, 8, 3, 1),  -- Technician 3 has 1 switch
(8, 8, 7, 1),  -- Technician 3 has 1 fiber optic cable
(9, 8, 11, 1); -- Technician 3 has 1 cable tester

-- ============================================================================
-- 9. MATERIAL_REQUESTS TABLE - Material requests from technicians
-- ============================================================================
INSERT INTO material_requests (id, description, user_id, applications_id, material_id, connection_order_id, technician_order_id, saff_order_id, quantity, price, total_price) VALUES
(1, 'Router kerak yangi ulanish uchun', 6, 1, 1, 1, NULL, NULL, 1, 350000, 350000),
(2, 'ONT kerak fiber ulanish uchun', 6, 2, 4, 2, NULL, NULL, 1, 280000, 280000),
(3, 'Kabel va konnektorlar', 7, 3, 6, NULL, 1, NULL, 1, 85000, 85000),
(4, 'RJ45 konnektorlar', 7, 3, 8, NULL, 1, NULL, 5, 25000, 125000),
(5, 'Switch 8-port kerak', 8, 4, 3, NULL, 2, NULL, 1, 420000, 420000),

-- Additional material requests for comprehensive testing
(6, 'Fiber optik kabel kerak - VIP mijoz uchun', 6, 1, 18, 1, NULL, NULL, 2, 2500000, 5000000),
(7, 'Network switch sorovi - korporativ mijoz', 7, 2, 19, 2, NULL, NULL, 1, 1500000, 1500000),
(8, 'WiFi router - standart ulanish uchun', 8, 3, 20, 3, NULL, NULL, 3, 450000, 1350000),
(9, 'Ethernet kabel - rad etildi', 6, 4, 21, 4, NULL, NULL, 5, 180000, 900000),
(10, 'Power adapter sorovi - biznes mijoz', 7, 5, 22, 5, NULL, NULL, 10, 80000, 800000),
(11, 'Antenna kerak - VIP ulanish', 8, 1, 23, NULL, 3, NULL, 1, 350000, 350000),
(12, 'Coaxial kabel - korporativ', 6, 2, 24, NULL, 4, NULL, 2, 220000, 440000),
(13, 'Signal amplifier - standart', 7, 3, 25, NULL, 5, NULL, 1, 650000, 650000),
(14, 'Test material - economy', 8, 4, 26, NULL, NULL, 1, 3, 100000, 300000),
(15, 'Test material 2 - enterprise', 6, 5, 27, NULL, NULL, 2, 2, 150000, 300000);

-- ============================================================================
-- 10. CONNECTIONS TABLE - Internal connections/communications
-- ============================================================================
INSERT INTO connections (id, sender_id, recipient_id, connecion_id, technician_id, saff_id, created_at, updated_at, sender_status, recipient_status) VALUES
(1, 3, 6, 1, 6, 1, NOW() - INTERVAL '2 days', NOW(), 'sent', 'received'),
(2, 4, 7, 2, 7, 2, NOW() - INTERVAL '1 day', NOW(), 'sent', 'pending'),
(3, 5, 8, 3, 8, 3, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days', 'completed', 'completed'),
(4, 3, 6, 4, 6, 4, NOW() - INTERVAL '3 hours', NOW(), 'sent', 'in_progress'),
(5, 12, 11, 5, NULL, 5, NOW() - INTERVAL '1 hour', NOW(), 'sent', 'pending');

-- ============================================================================
-- 11. REPORTS TABLE - System reports
-- ============================================================================
INSERT INTO reports (id, title, description, created_by, created_at, updated_at) VALUES
(1, 'Kunlik hisobot', 'Bugungi kun boyicha umumiy statistika', 111111111, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
(2, 'Haftalik material hisoboti', 'Hafta davomida ishlatilingan materiallar', 999999999, NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days'),
(3, 'Texnik xizmat hisoboti', 'Texnik xizmatlar boyicha hisobot', 666666666, NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
(4, 'Mijozlar reytingi', 'Mijozlar tomonidan berilgan reytinglar', 333333333, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
(5, 'Aylık umumiy hisobot', 'Oy davomida amalga oshirilgan ishlar', 111111111, NOW() - INTERVAL '30 days', NOW() - INTERVAL '30 days');

-- ============================================================================
-- 12. AKT_DOCUMENTS TABLE - Document management
-- ============================================================================
INSERT INTO akt_documents (id, request_id, request_type, akt_number, file_path, file_hash, created_at, sent_to_client_at) VALUES
(1, 1, 'connection', 'AKT-2024-001', '/documents/akt_connection_001.pdf', 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6', NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day'),
(2, 2, 'connection', 'AKT-2024-002', '/documents/akt_connection_002.pdf', 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7', NOW() - INTERVAL '1 day', NULL),
(3, 1, 'technician', 'AKT-2024-003', '/documents/akt_technician_001.pdf', 'c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8', NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 days'),
(4, 2, 'connection', 'AKT-2024-004', '/documents/akt_connection_003.pdf', 'd4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9', NOW() - INTERVAL '5 days', NOW() - INTERVAL '3 days'),
(5, 2, 'technician', 'AKT-2024-005', '/documents/akt_technician_002.pdf', 'e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0', NOW() - INTERVAL '2 hours', NULL);

-- ============================================================================
-- 13. AKT_RATINGS TABLE - Document ratings
-- ============================================================================
INSERT INTO akt_ratings (id, request_id, request_type, rating, comment, created_at) VALUES
(1, 1, 'connection', 5, 'Juda yaxshi xizmat', NOW() - INTERVAL '1 day'),
(2, 2, 'connection', 4, 'Yaxshi, lekin biroz kech', NOW() - INTERVAL '3 days'),
(3, 1, 'technician', 5, 'Texnik juda professional', NOW() - INTERVAL '2 days'),
(4, 2, 'technician', 3, 'Ortacha xizmat', NOW() - INTERVAL '2 hours'),
(5, 1, 'connection', 5, 'Mukammal ishlov', NOW() - INTERVAL '3 days');

-- ============================================================================
-- Update sequences to avoid conflicts
-- ============================================================================
SELECT setval('tarif_id_seq', (SELECT MAX(id) FROM tarif));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('materials_id_seq', (SELECT MAX(id) FROM materials));
SELECT setval('connection_orders_id_seq', (SELECT MAX(id) FROM connection_orders));
SELECT setval('technician_orders_id_seq', (SELECT MAX(id) FROM technician_orders));
SELECT setval('saff_orders_id_seq', (SELECT MAX(id) FROM saff_orders));
SELECT setval('smart_service_orders_id_seq', (SELECT MAX(id) FROM smart_service_orders));
SELECT setval('material_and_technician_id_seq', (SELECT MAX(id) FROM material_and_technician));
SELECT setval('material_requests_id_seq', (SELECT MAX(id) FROM material_requests));
SELECT setval('connections_id_seq', (SELECT MAX(id) FROM connections));
SELECT setval('reports_id_seq', (SELECT MAX(id) FROM reports));
SELECT setval('akt_documents_id_seq', (SELECT MAX(id) FROM akt_documents));
SELECT setval('akt_ratings_id_seq', (SELECT MAX(id) FROM akt_ratings));

-- ============================================================================
-- VERIFICATION QUERIES - Run these to verify data insertion
-- ============================================================================
-- SELECT 'Users count: ' || COUNT(*) FROM users;
-- SELECT 'Materials count: ' || COUNT(*) FROM materials;
-- SELECT 'Connection orders count: ' || COUNT(*) FROM connection_orders;
-- SELECT 'Technician orders count: ' || COUNT(*) FROM technician_orders;
-- SELECT 'Materials with low stock (<=10): ' || COUNT(*) FROM materials WHERE quantity <= 10 AND quantity > 0;
-- SELECT 'Materials out of stock: ' || COUNT(*) FROM materials WHERE quantity = 0;

COMMIT;

-- ============================================================================
-- END OF TEST DATA FILE
-- ============================================================================