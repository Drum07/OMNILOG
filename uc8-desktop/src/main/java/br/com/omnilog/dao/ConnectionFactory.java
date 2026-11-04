package br.com.omnilog.dao;
import java.sql.*;
/** Reads connection settings from environment; never hard-code credentials. */
public final class ConnectionFactory {private ConnectionFactory(){}public static Connection get() throws SQLException {String host=env("DB_HOST","127.0.0.1"),port=env("DB_PORT","3306"),db=env("DB_NAME","omnilog_hub");return DriverManager.getConnection("jdbc:mysql://"+host+":"+port+"/"+db+"?useSSL=true&serverTimezone=UTC",env("DB_USER","omnilog_app"),env("DB_PASSWORD",""));}private static String env(String k,String d){String v=System.getenv(k);return v==null?d:v;}}
