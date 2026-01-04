//! 고속 백테스팅 엔진 CLI
//!
//! 사용법:
//! ```bash
//! cargo run --release -- --data data/kospi.csv --strategy momentum
//! ```

use clap::Parser;
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

mod engine;
mod data;
mod strategy;

use engine::BacktestEngine;
use data::DataLoader;
use strategy::Strategy;

/// 고속 백테스팅 엔진
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// 데이터 파일 경로 (CSV)
    #[arg(short, long)]
    data: String,

    /// 전략 이름
    #[arg(short, long, default_value = "momentum")]
    strategy: String,

    /// 초기 자본금
    #[arg(short, long, default_value_t = 10_000_000)]
    capital: i64,

    /// 수수료율 (%)
    #[arg(short = 'f', long, default_value_t = 0.015)]
    fee: f64,

    /// 병렬 처리 스레드 수
    #[arg(short = 't', long)]
    threads: Option<usize>,
}

fn main() -> anyhow::Result<()> {
    // 로깅 초기화
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .finish();
    tracing::subscriber::set_global_default(subscriber)?;

    let args = Args::parse();

    info!("백테스팅 엔진 시작");
    info!("데이터: {}", args.data);
    info!("전략: {}", args.strategy);
    info!("초기 자본: {} 원", args.capital);
    info!("수수료: {}%", args.fee);

    // 스레드 수 설정
    if let Some(threads) = args.threads {
        rayon::ThreadPoolBuilder::new()
            .num_threads(threads)
            .build_global()?;
        info!("스레드 수: {}", threads);
    }

    // TODO: 실제 백테스트 로직 구현
    // let data = DataLoader::load_csv(&args.data)?;
    // let strategy = Strategy::from_name(&args.strategy)?;
    // let engine = BacktestEngine::new(args.capital, args.fee);
    // let result = engine.run(&data, &strategy)?;
    // println!("{}", result);

    info!("백테스팅 완료");
    Ok(())
}

