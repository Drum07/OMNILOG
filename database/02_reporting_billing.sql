USE omnilog_hub;
-- MySQL does not provide native materialized views. This summary table is refreshed by procedure.
CREATE TABLE IF NOT EXISTS daily_billing_summary (
 billing_date DATE PRIMARY KEY,
 paid_orders BIGINT UNSIGNED NOT NULL DEFAULT 0,
 gross_amount DECIMAL(15,2) NOT NULL DEFAULT 0,
 refreshed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_generate_daily_billing$$
CREATE PROCEDURE sp_generate_daily_billing(IN p_billing_date DATE)
BEGIN
 INSERT INTO daily_billing_summary(billing_date,paid_orders,gross_amount)
 SELECT p_billing_date,COUNT(DISTINCT o.order_id),COALESCE(SUM(p.amount),0)
 FROM orders o JOIN payments p ON p.order_id=o.order_id
 WHERE DATE(COALESCE(p.paid_at,p.created_at))=p_billing_date AND p.payment_status='PAID'
 ON DUPLICATE KEY UPDATE paid_orders=VALUES(paid_orders),gross_amount=VALUES(gross_amount),refreshed_at=CURRENT_TIMESTAMP;
END$$
DELIMITER ;
CREATE INDEX idx_payments_paid_at_status ON payments(payment_status,paid_at);
CREATE INDEX idx_deliveries_tracking_status ON deliveries(tracking_code,delivery_status);
-- Example: CALL sp_generate_daily_billing(CURRENT_DATE - INTERVAL 1 DAY);
