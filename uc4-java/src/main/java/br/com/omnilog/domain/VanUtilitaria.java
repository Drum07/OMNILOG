package br.com.omnilog.domain;
import java.math.BigDecimal;
public final class VanUtilitaria extends Veiculo {
 public VanUtilitaria(String id,BigDecimal capacidade){super(id,capacidade);}
 @Override public BigDecimal calcularAutonomiaKm(BigDecimal carga){validar(BigDecimal.ZERO,carga);return new BigDecimal("600").subtract(carga.multiply(new BigDecimal("0.04"))).max(BigDecimal.ZERO);}
 @Override public BigDecimal calcularCustoFrete(BigDecimal km,BigDecimal carga){validar(km,carga);return km.multiply(new BigDecimal("2.10")).add(carga.multiply(new BigDecimal("0.20"))).setScale(2,java.math.RoundingMode.HALF_UP);}
}
