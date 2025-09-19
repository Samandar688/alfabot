-- saff_orders jadvali uchun namunaviy ma'lumotlar
-- Ushbu faylda to'g'ri enum qiymatlari va ma'lumot turlari ishlatilgan

-- Avval mavjud ma'lumotlarni tozalash (ixtiyoriy)
-- TRUNCATE TABLE saff_orders RESTART IDENTITY CASCADE;

-- saff_orders jadvaliga namunaviy ma'lumotlar qo'shish
-- Haqiqiy user_id larni ishlatamiz (users jadvalidan)
INSERT INTO saff_orders (user_id, phone, region, abonent_id, tarif_id, address, description, status, type_of_zayavka, is_active, created_at, updated_at) VALUES 
-- Ulanish xizmatlari (connection)
(1, '+998901234567', 1, '1001', 1, 'Chilonzor tumani, 45-uy', 'Internet ulanishi sozlamasi kerak', 'in_call_center', 'connection', true, '2025-01-19 14:00:00+05:00', '2025-01-19 14:00:00+05:00'),
(3, '+998912345678', 2, '1002', 2, 'Registon ko''chasi, 12-uy', 'Router o''rnatish talab qilinadi', 'in_manager', 'connection', true, '2025-01-18 09:30:00+05:00', '2025-01-18 09:30:00+05:00'),
(5, '+998933456789', 3, '1003', 3, 'Alpomish mahallasi, 5-uy', 'Yangi internet liniyasi o''tkazish kerak', 'in_controller', 'connection', true, '2025-01-17 11:15:00+05:00', '2025-01-18 10:00:00+05:00'),
(6, '+998944567890', 4, '1004', 4, 'Yuksalish ko''chasi, 33-uy', 'Fiber optik kabel o''rnatish', 'in_technician', 'connection', true, '2025-01-16 15:20:00+05:00', '2025-01-17 12:00:00+05:00'),
(14, '+998957890123', 5, '1005', 1, 'Navoiy prospekti, 8-uy', 'Yangi tarifga o''tish uchun so''rov', 'completed', 'connection', false, '2025-01-15 10:45:00+05:00', '2025-01-16 14:30:00+05:00'),

-- Texnik xizmatlar (technician)
(6, '+998966789012', 1, '1006', 2, 'Mirzo Ulug''bek tumani, 22-uy', 'Internet tezligi past, tekshirish kerak', 'in_call_center', 'technician', true, '2025-01-19 16:20:00+05:00', '2025-01-19 16:20:00+05:00'),
(7, '+998977890123', 2, '1007', 3, 'Shayxontohur tumani, 67-uy', 'Kabel uzilgan, almashtirish kerak', 'in_controller', 'technician', true, '2025-01-18 13:45:00+05:00', '2025-01-19 08:15:00+05:00'),
(8, '+998988901234', 3, '1008', 4, 'Bektemir tumani, 15-uy', 'Router ishlamayapti, ta''mirlash kerak', 'in_technician', 'technician', true, '2025-01-17 12:30:00+05:00', '2025-01-18 14:20:00+05:00'),
(9, '+998999012345', 4, '1009', 1, 'Sergeli tumani, 89-uy', 'Signal kuchsiz, antennani sozlash kerak', 'in_technician', 'technician', true, '2025-01-16 09:10:00+05:00', '2025-01-17 16:45:00+05:00'),
(11, '+998901112233', 5, '1010', 2, 'Yunusobod tumani, 34-uy', 'Modem almashtirish kerak', 'completed', 'technician', false, '2025-01-15 14:25:00+05:00', '2025-01-16 11:30:00+05:00'),

-- Qo'shimcha namunaviy ma'lumotlar
(12, '+998902223344', 1, '1011', 3, 'Olmazor tumani, 56-uy', 'Wi-Fi signali kuchsiz', 'in_technician', 'technician', true, '2025-01-19 11:00:00+05:00', '2025-01-19 11:00:00+05:00'),
(13, '+998903334455', 2, '1012', 4, 'Yashnobod tumani, 78-uy', 'Yangi ulanish kerak', 'in_controller', 'connection', true, '2025-01-18 15:30:00+05:00', '2025-01-19 09:45:00+05:00'),
(62, '+998904445566', 3, '1013', 1, 'Uchtepa tumani, 23-uy', 'Internet uzilib qoladi', 'in_manager', 'technician', true, '2025-01-17 08:15:00+05:00', '2025-01-17 08:15:00+05:00'),
(63, '+998905556677', 4, '1014', 2, 'Hamza tumani, 45-uy', 'Tarif o''zgartirish kerak', 'in_manager', 'connection', true, '2025-01-16 13:20:00+05:00', '2025-01-17 10:30:00+05:00'),
(64, '+998906667788', 5, '1015', 3, 'Qo''yliq tumani, 67-uy', 'Kabel ta''mirlash', 'in_manager', 'technician', true, '2025-01-15 16:40:00+05:00', '2025-01-16 12:15:00+05:00');

-- Sequence ni yangilash (agar kerak bo'lsa)
-- SELECT setval('saff_orders_id_seq', (SELECT MAX(id) FROM saff_orders));

-- Ma'lumotlarni tekshirish
-- SELECT COUNT(*) as total_records FROM saff_orders;
-- SELECT status, COUNT(*) as count FROM saff_orders GROUP BY status;
-- SELECT type_of_zayavka, COUNT(*) as count FROM saff_orders GROUP BY type_of_zayavka;