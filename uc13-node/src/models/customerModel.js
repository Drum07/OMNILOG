import {pool} from '../config/db.js';
export async function listCustomers({limit=25,offset=0,search=''}){const like=`%${search}%`;const [rows]=await pool.execute('SELECT customer_id,full_name,email,phone,is_active,created_at FROM customers WHERE full_name LIKE ? OR email LIKE ? ORDER BY customer_id DESC LIMIT ? OFFSET ?',[like,like,limit,offset]);return rows;}
export async function createCustomer({full_name,email,phone}){const [r]=await pool.execute('INSERT INTO customers(full_name,email,phone) VALUES(?,?,?)',[full_name,email,phone||null]);return r.insertId;}
export async function getCustomer(id){const [r]=await pool.execute('SELECT customer_id,full_name,email,phone,is_active,created_at FROM customers WHERE customer_id=?',[id]);return r[0]||null;}
