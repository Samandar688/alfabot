ALTER TYPE saff_order_status
  ADD VALUE IF NOT EXISTS 'in_technician_work' AFTER 'in_technician';
