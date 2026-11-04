package br.com.omnilog.domain;
import java.math.BigDecimal;
public final class CaminhaoFrigorifico extends Veiculo {
 public CaminhaoFrigorifico(String id,BigDecimal capacidade){super(id,capacidade);}
 @Override public BigDecimal calcularAutonomiaKm(BigDecimal carga){validar(BigDecimal.ZERO,carga);return new BigDecimal("900").subtract(carga.multiply(new BigDecimal("0.02"))).max(BigDecimal.ZERO);}
 @Override public BigDecimal calcularCustoFrete(BigDecimal km,BigDecimal carga){validar(km,carga);return km.multiply(new BigDecimal("4.80")).add(carga.multiply(new BigDecimal("0.35"))).setScale(2,java.math.RoundingMode.HALF_UP);}
}
