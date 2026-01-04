//! 백테스트 엔진 모듈

use rust_decimal::Decimal;
use rust_decimal_macros::dec;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::data::StockData;
use crate::strategy::{Signal, Strategy};

/// 백테스트 설정
#[derive(Debug, Clone)]
pub struct BacktestConfig {
    /// 초기 자본금
    pub initial_capital: Decimal,
    /// 수수료율 (0.00015 = 0.015%)
    pub commission_rate: Decimal,
    /// 슬리피지 (0.001 = 0.1%)
    pub slippage: Decimal,
    /// 최대 보유 종목 수
    pub max_positions: usize,
    /// 종목당 최대 투자 비율
    pub max_position_size: Decimal,
}

impl Default for BacktestConfig {
    fn default() -> Self {
        Self {
            initial_capital: dec!(10_000_000),
            commission_rate: dec!(0.00015),
            slippage: dec!(0.001),
            max_positions: 10,
            max_position_size: dec!(0.1),
        }
    }
}

/// 포지션 정보
#[derive(Debug, Clone)]
pub struct Position {
    pub symbol: String,
    pub quantity: i64,
    pub avg_price: Decimal,
    pub current_price: Decimal,
}

impl Position {
    pub fn market_value(&self) -> Decimal {
        self.current_price * Decimal::from(self.quantity)
    }

    pub fn unrealized_pnl(&self) -> Decimal {
        (self.current_price - self.avg_price) * Decimal::from(self.quantity)
    }

    pub fn unrealized_pnl_pct(&self) -> Decimal {
        if self.avg_price.is_zero() {
            dec!(0)
        } else {
            (self.current_price - self.avg_price) / self.avg_price * dec!(100)
        }
    }
}

/// 백테스트 결과
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BacktestResult {
    /// 총 수익률 (%)
    pub total_return: f64,
    /// 연환산 수익률 (%)
    pub cagr: f64,
    /// 샤프 비율
    pub sharpe_ratio: f64,
    /// 최대 낙폭 (%)
    pub max_drawdown: f64,
    /// 승률 (%)
    pub win_rate: f64,
    /// 총 거래 횟수
    pub total_trades: usize,
    /// 일별 자산 가치
    pub equity_curve: Vec<f64>,
}

/// 백테스트 엔진
pub struct BacktestEngine {
    config: BacktestConfig,
    cash: Decimal,
    positions: HashMap<String, Position>,
    equity_history: Vec<Decimal>,
    trade_count: usize,
    winning_trades: usize,
}

impl BacktestEngine {
    pub fn new(config: BacktestConfig) -> Self {
        let initial_cash = config.initial_capital;
        Self {
            config,
            cash: initial_cash,
            positions: HashMap::new(),
            equity_history: Vec::new(),
            trade_count: 0,
            winning_trades: 0,
        }
    }

    /// 현재 총 자산 가치
    pub fn total_equity(&self) -> Decimal {
        let positions_value: Decimal = self.positions.values().map(|p| p.market_value()).sum();
        self.cash + positions_value
    }

    /// 백테스트 실행
    pub fn run<S: Strategy>(&mut self, data: &StockData, strategy: &S) -> BacktestResult {
        for (i, candle) in data.candles.iter().enumerate() {
            // 포지션 가격 업데이트
            if let Some(pos) = self.positions.get_mut(&data.symbol) {
                pos.current_price = candle.close;
            }

            // 전략 시그널 계산
            let signal = strategy.generate_signal(&data.candles[..=i]);

            // 시그널에 따른 주문 실행
            match signal {
                Signal::Buy => self.execute_buy(&data.symbol, candle.close),
                Signal::Sell => self.execute_sell(&data.symbol, candle.close),
                Signal::Hold => {}
            }

            // 자산 가치 기록
            self.equity_history.push(self.total_equity());
        }

        self.calculate_result()
    }

    fn execute_buy(&mut self, symbol: &str, price: Decimal) {
        // 이미 포지션이 있으면 스킵
        if self.positions.contains_key(symbol) {
            return;
        }

        // 최대 포지션 수 체크
        if self.positions.len() >= self.config.max_positions {
            return;
        }

        // 투자 금액 계산 (자산의 max_position_size%)
        let invest_amount = self.total_equity() * self.config.max_position_size;
        let slippage_price = price * (Decimal::ONE + self.config.slippage);
        let quantity = (invest_amount / slippage_price).floor().to_string().parse::<i64>().unwrap_or(0);

        if quantity <= 0 {
            return;
        }

        let cost = slippage_price * Decimal::from(quantity);
        let commission = cost * self.config.commission_rate;
        let total_cost = cost + commission;

        if total_cost > self.cash {
            return;
        }

        self.cash -= total_cost;
        self.positions.insert(
            symbol.to_string(),
            Position {
                symbol: symbol.to_string(),
                quantity,
                avg_price: slippage_price,
                current_price: price,
            },
        );
        self.trade_count += 1;
    }

    fn execute_sell(&mut self, symbol: &str, price: Decimal) {
        if let Some(position) = self.positions.remove(symbol) {
            let slippage_price = price * (Decimal::ONE - self.config.slippage);
            let proceeds = slippage_price * Decimal::from(position.quantity);
            let commission = proceeds * self.config.commission_rate;
            let net_proceeds = proceeds - commission;

            self.cash += net_proceeds;
            self.trade_count += 1;

            // 수익 거래 카운트
            if slippage_price > position.avg_price {
                self.winning_trades += 1;
            }
        }
    }

    fn calculate_result(&self) -> BacktestResult {
        let initial = self.config.initial_capital;
        let final_equity = self.total_equity();
        
        // 총 수익률
        let total_return = ((final_equity - initial) / initial * dec!(100))
            .to_string()
            .parse::<f64>()
            .unwrap_or(0.0);

        // 최대 낙폭 계산
        let max_drawdown = self.calculate_max_drawdown();

        // 승률
        let win_rate = if self.trade_count > 0 {
            (self.winning_trades as f64 / self.trade_count as f64) * 100.0
        } else {
            0.0
        };

        // 샤프 비율 계산 (간단 버전)
        let sharpe_ratio = self.calculate_sharpe_ratio();

        // CAGR 계산 (일 단위)
        let days = self.equity_history.len() as f64;
        let years = days / 252.0;
        let cagr = if years > 0.0 {
            ((final_equity / initial).to_string().parse::<f64>().unwrap_or(1.0)).powf(1.0 / years) - 1.0
        } else {
            0.0
        } * 100.0;

        BacktestResult {
            total_return,
            cagr,
            sharpe_ratio,
            max_drawdown,
            win_rate,
            total_trades: self.trade_count,
            equity_curve: self.equity_history.iter()
                .map(|e| e.to_string().parse::<f64>().unwrap_or(0.0))
                .collect(),
        }
    }

    fn calculate_max_drawdown(&self) -> f64 {
        let mut max_equity = Decimal::ZERO;
        let mut max_dd = Decimal::ZERO;

        for equity in &self.equity_history {
            if *equity > max_equity {
                max_equity = *equity;
            }
            let dd = (max_equity - *equity) / max_equity * dec!(100);
            if dd > max_dd {
                max_dd = dd;
            }
        }

        max_dd.to_string().parse::<f64>().unwrap_or(0.0)
    }

    fn calculate_sharpe_ratio(&self) -> f64 {
        if self.equity_history.len() < 2 {
            return 0.0;
        }

        // 일별 수익률 계산
        let returns: Vec<f64> = self.equity_history
            .windows(2)
            .map(|w| {
                let prev = w[0].to_string().parse::<f64>().unwrap_or(1.0);
                let curr = w[1].to_string().parse::<f64>().unwrap_or(1.0);
                (curr - prev) / prev
            })
            .collect();

        let mean: f64 = returns.iter().sum::<f64>() / returns.len() as f64;
        let variance: f64 = returns.iter().map(|r| (r - mean).powi(2)).sum::<f64>() / returns.len() as f64;
        let std_dev = variance.sqrt();

        if std_dev == 0.0 {
            return 0.0;
        }

        // 연환산 (252 거래일 기준)
        (mean / std_dev) * (252.0_f64).sqrt()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config() {
        let config = BacktestConfig::default();
        assert_eq!(config.initial_capital, dec!(10_000_000));
        assert_eq!(config.max_positions, 10);
    }
}

