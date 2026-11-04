#[derive(Debug, Clone, PartialEq)]
pub enum PanelItemType { AppLauncher, Taskbar, SystemTray, Clock, WorkspaceIndicator, Separator }
#[derive(Debug, Clone)]
pub struct PanelItem { pub id: String, pub item_type: PanelItemType, pub visible: bool, pub position: u32 }
impl PanelItem {
    pub fn new(id: &str, item_type: PanelItemType, position: u32) -> Self {
        Self { id: id.to_string(), item_type, visible: true, position }
    }
}
#[derive(Debug, Clone, PartialEq)]
pub enum PanelPosition { Top, Bottom, Left, Right }
pub struct Panel { items: Vec<PanelItem>, position: PanelPosition, height: u32 }
impl Panel {
    pub fn new(position: PanelPosition) -> Self { Self { items: Vec::new(), position, height: 36 } }
    pub fn add_item(&mut self, item: PanelItem) { self.items.push(item); }
    pub fn visible_count(&self) -> usize { self.items.iter().filter(|i| i.visible).count() }
    pub fn position(&self) -> &PanelPosition { &self.position }
    pub fn height(&self) -> u32 { self.height }
    pub fn item_count(&self) -> usize { self.items.len() }
}
impl Default for Panel { fn default() -> Self { Self::new(PanelPosition::Top) } }
