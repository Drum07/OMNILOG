package br.com.omnilog.domain;
import java.math.BigDecimal;
public final class DroneEntrega extends Veiculo {
 public DroneEntrega(String id,BigDecimal capacidade){super(id,capacidade);}
 @Override public BigDecimal calcularAutonomiaKm(BigDecimal carga){validar(BigDecimal.ZERO,carga);return new BigDecimal("30").subtract(carga.multiply(new BigDecimal("0.8"))).max(BigDecimal.ZERO);}
 @Override public BigDecimal calcularCustoFrete(BigDecimal km,BigDecimal carga){validar(km,carga);return km.multiply(new BigDecimal("1.50")).add(carga.multiply(new BigDecimal("1.25"))).setScale(2,java.math.RoundingMode.HALF_UP);}
}
