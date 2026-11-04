import mysql from 'mysql2/promise';
export const pool=mysql.createPool({host:process.env.DB_HOST||'127.0.0.1',port:Number(process.env.DB_PORT||3306),user:process.env.DB_USER,database:process.env.DB_NAME||'omnilog_hub',password:process.env.DB_PASSWORD,waitForConnections:true,connectionLimit:10,queueLimit:0,decimalNumbers:true});
