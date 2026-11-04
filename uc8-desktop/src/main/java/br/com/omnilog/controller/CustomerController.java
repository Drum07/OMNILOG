package br.com.omnilog.controller;import br.com.omnilog.dao.CustomerDao;import br.com.omnilog.model.Customer;import java.sql.SQLException;import java.util.List;
public final class CustomerController {private final CustomerDao dao=new CustomerDao();public List<Customer> pesquisar(String termo)throws SQLException{return dao.search(termo,50,0);}}
