package br.com.omnilog.domain;
import java.math.BigDecimal;
/** Domain contract: subclasses define autonomy and freight calculation. */
public abstract class Veiculo {
 private final String identificador; private final BigDecimal capacidadeKg;
 protected Veiculo(String identificador, BigDecimal capacidadeKg) {
  if (identificador == null || identificador.isBlank()) throw new IllegalArgumentException("Identificador obrigatório");
  if (capacidadeKg == null || capacidadeKg.signum() <= 0) throw new IllegalArgumentException("Capacidade deve ser positiva");
  this.identificador=identificador; this.capacidadeKg=capacidadeKg;
 }
 public final String getIdentificador(){return identificador;} public final BigDecimal getCapacidadeKg(){return capacidadeKg;}
 public abstract BigDecimal calcularAutonomiaKm(BigDecimal cargaKg);
 public abstract BigDecimal calcularCustoFrete(BigDecimal distanciaKm, BigDecimal cargaKg);
 protected final void validar(BigDecimal distanciaKm, BigDecimal cargaKg){if(distanciaKm==null||distanciaKm.signum()<0||cargaKg==null||cargaKg.signum()<0||cargaKg.compareTo(capacidadeKg)>0)throw new IllegalArgumentException("Distância/carga inválida ou acima da capacidade");}
}
