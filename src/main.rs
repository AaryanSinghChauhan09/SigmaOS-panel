//! SigmaOS-panel - SigmaOS Component CLI
//!
//! Command-line interface for SigmaOS-panel component.

use anyhow::Result;
use clap::{Parser, Subcommand};
use log::info;
use panel::{Component, ComponentStatus, Config, panel};

#[derive(Parser)]
#[command(name = "panel")]
#[command(about = "SigmaOS SigmaOS-panel component", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize the component
    Init {
        /// Enable debug mode
        #[arg(short, long)]
        debug: bool,
    },
    /// Start the component
    Start,
    /// Stop the component
    Stop,
    /// Get component status
    Status,
    /// Run the component
    Run {
        /// Enable debug mode
        #[arg(short, long)]
        debug: bool,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    
    let config = Config::default();
    let mut component = panel::new(config);

    match cli.command {
        Commands::Init { debug } => {
            if debug {
                println!("Initializing SigmaOS-panel in debug mode...");
            } else {
                println!("Initializing SigmaOS-panel...");
            }
            component.initialize()?;
            println!("SigmaOS-panel initialized successfully");
        }
        Commands::Start => {
            component.initialize()?;
            component.start()?;
            println!("SigmaOS-panel started successfully");
        }
        Commands::Stop => {
            component.stop()?;
            println!("SigmaOS-panel stopped successfully");
        }
        Commands::Status => {
            let status = component.status();
            println!("SigmaOS-panel status: {:?}", status);
        }
        Commands::Run { debug } => {
            if debug {
                println!("Running SigmaOS-panel in debug mode...");
            } else {
                println!("Running SigmaOS-panel...");
            }
            component.initialize()?;
            component.start()?;
            println!("SigmaOS-panel is running. Press Ctrl+C to stop.");
            
            // Keep running
            tokio::runtime::Runtime::new()?.block_on(async {
                tokio::signal::ctrl_c().await.unwrap();
                info!("Received Ctrl+C, shutting down...");
            });
            
            component.stop()?;
            println!("SigmaOS-panel stopped");
        }
    }

    Ok(())
}
