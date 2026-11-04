use sigmaos_panel::{Config, PanelComponent, Component};
fn main() {
    env_logger::init();
    let mut c = PanelComponent::new(Config::default());
    if let Err(e) = c.initialize() { eprintln!("Failed: {}", e); std::process::exit(1); }
    println!("SigmaOS panel running");
    let _ = c.shutdown();
}
