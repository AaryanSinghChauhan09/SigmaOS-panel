use sigmaos_panel::{Config, Panel, PanelComponent, PanelItem, PanelItemType, PanelPosition, Component};

#[test]
fn test_panel_default_position_aaa() {
    let panel = Panel::default();
    assert_eq!(panel.position(), &PanelPosition::Top);
    assert_eq!(panel.height(), 36);
}

#[test]
fn test_panel_add_items_aaa() {
    let mut panel = Panel::new(PanelPosition::Top);
    panel.add_item(PanelItem::new("launcher", PanelItemType::AppLauncher, 0));
    panel.add_item(PanelItem::new("taskbar", PanelItemType::Taskbar, 1));
    panel.add_item(PanelItem::new("tray", PanelItemType::SystemTray, 2));
    assert_eq!(panel.item_count(), 3);
    assert_eq!(panel.visible_count(), 3);
}

#[test]
fn test_panel_hidden_item_aaa() {
    let mut panel = Panel::new(PanelPosition::Bottom);
    let mut item = PanelItem::new("clock", PanelItemType::Clock, 0);
    item.visible = false;
    panel.add_item(item);
    assert_eq!(panel.visible_count(), 0);
}

#[test]
fn test_component_lifecycle_aaa() {
    let mut c = PanelComponent::new(Config::default());
    assert!(c.initialize().is_ok());
    assert!(c.health_check().is_ok());
    assert!(c.shutdown().is_ok());
}

#[test]
fn test_component_name_aaa() {
    let c = PanelComponent::new(Config::default());
    assert_eq!(c.name(), "sigmaos-panel");
}
