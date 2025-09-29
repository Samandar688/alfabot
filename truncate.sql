-- Barcha jadvallarni truncate qilish (id larni ham 1 dan boshlab qayta hisoblash uchun RESTART IDENTITY)
TRUNCATE akt_documents,
         akt_ratings,
         connection_orders,
         connections,
         material_and_technician,
         material_requests,
         reports,
         saff_orders,
         smart_service_orders,
         technician_orders,
         users
RESTART IDENTITY CASCADE;
