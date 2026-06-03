# Brigador Killers Demo - Lua脚本目录

> 生成日期: 2026-06-03

本目录文档记录了 `assets/scripts` 文件夹下的所有 Lua 脚本文件及其功能说明。

---

## 目录结构总览

```
assets/scripts/
├── 根目录脚本
├── lib/ (核心库)
├── monads/ (动作链系统)
├── level_objects/ (关卡对象)
├── level_toolkit/ (关卡工具箱)
├── level_scripts/ (关卡脚本)
├── objectives/ (目标系统)
├── include/ (工具库)
├── data/ (数据文件)
├── helper/ (辅助脚本)
└── inventory/ (物品栏定义)
```

---

## 一、根目录脚本 (assets/scripts/)

| 文件 | 作用 |
|------|------|
| [FFI_Test.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/FFI_Test.lua) | FFI（Foreign Function Interface）测试脚本 |
| [demoscript.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/demoscript.lua) | 演示脚本 |
| [polyspawn.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/polyspawn.lua) | 多边形/多物体生成脚本 |
| [bktemplate_map_pickups.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/bktemplate_map_pickups.lua) | 地图拾取物模板 |
| [helper_patroldebug.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/helper_patroldebug.lua) | 巡逻调试辅助脚本 |

---

## 二、核心库 (assets/scripts/lib/)

| 文件 | 作用 |
|------|------|
| [util.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/util.lua) | 通用工具函数库（表操作、字符串处理等） |
| [callbacks.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/callbacks.lua) | 内置全局回调函数（对话、游戏变量、物品拾取等） |
| [collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/collider.lua) | 碰撞检测系统（圆形、矩形碰撞器） |
| [gamestate.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/gamestate.lua) | 游戏状态管理 |
| [dialogue.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/dialogue.lua) | 对话系统（对话框渲染、对话流程控制） |
| [monad.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/monad.lua) | 函数式编程monad系统（动作链执行） |
| [predicates.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/predicates.lua) | 谓词系统（条件判断、gvar/mvar变量访问） |
| [inventory.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/inventory.lua) | 库存和物品系统（物品、储物舱、掉落表） |
| [circle.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/circle.lua) | 圆形碰撞形状定义 |
| [rectangle.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/rectangle.lua) | 矩形碰撞形状定义 |
| [ellipse.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/ellipse.lua) | 椭圆碰撞形状定义 |
| [fadetoblack.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/fadetoblack.lua) | 黑屏/淡入淡出效果 |
| [objectivesui.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/objectivesui.lua) | 目标UI系统 |
| [keyitemtable.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/keyitemtable.lua) | 关键物品表 |
| [mapstate.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/mapstate.lua) | 地图状态管理 |
| [tablewriter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/tablewriter.lua) | 表写入工具 |
| [ephemeraltext.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/lib/ephemeraltext.lua) | 临时文本/提示系统 |

---

## 三、Monads（动作链系统）(assets/scripts/monads/)

| 文件 | 作用 |
|------|------|
| [dialogue.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/dialogue.lua) | 打开对话动作 |
| [open_exits.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/open_exits.lua) | 打开/关闭出口动作 |
| [on_enter_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/on_enter_collider.lua) | 进入碰撞器触发动作 |
| [on_exit_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/on_exit_collider.lua) | 退出碰撞器触发动作 |
| [board.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/board.lua) | 登船/进入载具动作 |
| [filter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/filter.lua) | 条件过滤器动作 |
| [maybe.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/maybe.lua) | Maybe条件分支动作 |
| [maybe_toggler.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/maybe_toggler.lua) | Maybe切换器动作 |
| [on_init.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/on_init.lua) | 初始化时执行动作 |
| [relay.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/relay.lua) | 动作中继/转发 |
| [set_gvar.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/set_gvar.lua) | 设置全局变量 |
| [toggle_gvar_bool.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/toggle_gvar_bool.lua) | 切换布尔变量 |
| [timer.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/timer.lua) | 计时器动作 |
| [unit_lock.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_lock.lua) | 锁定单位动作 |
| [load_next_phase.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/load_next_phase.lua) | 加载下一阶段 |
| [lose_level.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/lose_level.lua) | 关卡失败 |
| [action_on_limit.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/action_on_limit.lua) | 限制条件下执行动作 |
| [unit_spawn.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_spawn.lua) | 生成单位 |
| [unit_delete.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_delete.lua) | 删除单位 |
| [unit_set_state.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_set_state.lua) | 设置单位状态 |
| [unit_set_order.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_set_order.lua) | 设置单位指令 |
| [unit_teleport.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_teleport.lua) | 传送单位 |
| [unit_marker.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/unit_marker.lua) | 单位标记 |
| [key_unit_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/key_unit_collider.lua) | 关键单位碰撞器 |
| [play_sound.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/play_sound.lua) | 播放音效 |
| [toggle_text.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/toggle_text.lua) | 切换文本显示 |
| [toggle_gate.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/toggle_gate.lua) | 切换门/闸门 |
| [hide_console.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/hide_console.lua) | 隐藏控制台 |
| [disable_console.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/disable_console.lua) | 禁用控制台 |
| [dynamic_marker.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/dynamic_marker.lua) | 动态标记 |
| [action_on_button.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/monads/action_on_button.lua) | 按钮触发动作 |

---

## 四、关卡对象 (assets/scripts/level_objects/)

| 文件 | 作用 |
|------|------|
| [essential.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/essential.lua) | 核心/必需对象 |
| [test_marker.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/test_marker.lua) | 测试标记 |
| [static_marker.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/static_marker.lua) | 静态标记 |
| [point.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/point.lua) | 点对象 |
| [rectangle_area.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/rectangle_area.lua) | 矩形区域 |
| [script_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/script_collider.lua) | 脚本碰撞器 |
| [text_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/text_collider.lua) | 文本碰撞器 |
| [textcollider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/textcollider.lua) | 文本碰撞器（备用名） |
| [sound_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/sound_collider.lua) | 声音碰撞器 |
| [gvar_trigger.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/gvar_trigger.lua) | 游戏变量触发器 |
| [enable_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/enable_collider.lua) | 启用碰撞器 |
| [disable_suppression.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/disable_suppression.lua) | 禁用压制效果 |
| [disable_morale.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/disable_morale.lua) | 禁用士气系统 |
| [godmode.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/godmode.lua) | 无敌模式 |
| [disablesalvage.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/disablesalvage.lua) | 禁用回收系统 |
| [disableinventory.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/disableinventory.lua) | 禁用物品栏 |
| [door_group.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/door_group.lua) | 门组控制 |
| [door_console.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/door_console.lua) | 门控制台 |
| [interactable_console.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/interactable_console.lua) | 可交互控制台 |
| [dialogue_trigger.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/dialogue_trigger.lua) | 对话触发器 |
| [trigger_dialogue_death.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/trigger_dialogue_death.lua) | 死亡触发对话 |
| [mission_selector.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/mission_selector.lua) | 任务选择器 |
| [assassinate.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/assassinate.lua) | 暗杀目标 |
| [ordershelper.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/ordershelper.lua) | 指令辅助器 |
| [reset_character_on_defeat.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/reset_character_on_defeat.lua) | 失败时重置角色 |
| [reset_character_on_win.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/reset_character_on_win.lua) | 胜利时重置角色 |
| [steal_car.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/steal_car.lua) | 偷车功能 |
| [suit_valet.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/suit_valet.lua) | 套装/载具保管员 |
| [suit_valet_old.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/suit_valet_old.lua) | 旧版本套装保管员 |
| [level_music.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/level_music.lua) | 关卡音乐 |
| [delayed_spawn.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/delayed_spawn.lua) | 延迟生成 |
| [textoffset.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/textoffset.lua) | 文本偏移 |
| [offscreen_action.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/offscreen_action.lua) | 屏幕外动作 |
| [manufactory_zone.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/manufactory_zone.lua) | 制造区域 |
| [manufactory_console.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/manufactory_console.lua) | 制造控制台 |
| [apartment_cleanup.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_objects/apartment_cleanup.lua) | 公寓清理 |

---

## 五、关卡工具箱 (assets/scripts/level_toolkit/)

| 文件 | 作用 |
|------|------|
| [modify_gvar.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/modify_gvar.lua) | 修改游戏变量 |
| [unit_spawn.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/unit_spawn.lua) | 单位生成工具 |
| [unit_delete.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/unit_delete.lua) | 单位删除工具 |
| [load_next_level.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/load_next_level.lua) | 加载下一关 |
| [lose_level.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/lose_level.lua) | 关卡失败工具 |
| [callback_splitter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/callback_splitter.lua) | 回调分离器 |
| [dialogue_action.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/dialogue_action.lua) | 对话动作工具 |
| [play_sound.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/play_sound.lua) | 播放音效工具 |
| [do_nothing.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/do_nothing.lua) | 空操作（占位符） |
| [action_in_out_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/action_in_out_collider.lua) | 进出碰撞器动作 |
| [time_limit.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/time_limit.lua) | 时间限制工具 |
| [action_on_limit.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/action_on_limit.lua) | 限制条件动作工具 |
| [key_unit_collider.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/key_unit_collider.lua) | 关键单位碰撞器工具 |
| [toggle_text.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/toggle_text.lua) | 切换文本工具 |
| [dynamic_marker.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_toolkit/dynamic_marker.lua) | 动态标记工具 |

---

## 六、关卡脚本 (assets/scripts/level_scripts/)

| 文件 | 作用 |
|------|------|
| [mission_1_holgerpad.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/mission_1_holgerpad.lua) | 任务1 - Holgerpad |
| [trigger_exitopen.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/trigger_exitopen.lua) | 触发出口打开 |
| [bulver_orders.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/bulver_orders.lua) | Bulver指令 |
| [gvar_setter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/gvar_setter.lua) | 游戏变量设置器 |
| [gvar_win_setter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/gvar_win_setter.lua) | 胜利变量设置器 |
| [essential_setter.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/essential_setter.lua) | 核心对象设置器 |
| [selector_intro.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/selector_intro.lua) | 选择器介绍 |
| [brigador_heroes.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/brigador_heroes.lua) | Brigador英雄 |
| [e01_h00_m01_hospital.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h00_m01_hospital.lua) | 章节1任务1 - 医院 |
| [e01_h00_m01_wharf.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h00_m01_wharf.lua) | 章节1任务1 - 码头 |
| [e01_h00_m01_sadysidegate.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h00_m01_sadysidegate.lua) | 章节1任务1 - Sadyside门 |
| [e01_h00_m01_docweekend.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h00_m01_docweekend.lua) | 章节1任务1 - Doc周末 |
| [e01_h02_firstbase_tutorial.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h02_firstbase_tutorial.lua) | 章节1阶段2 - Firstbase教程 |
| [e01_h02_second_tutorial.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h02_second_tutorial.lua) | 章节1阶段2 - 第二教程 |
| [e01_h02_m00_corvidjunkyard.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/level_scripts/e01_h02_m00_corvidjunkyard.lua) | 章节1阶段2任务0 - Corvid垃圾场 |

---

## 七、目标系统 (assets/scripts/objectives/)

| 文件 | 作用 |
|------|------|
| [assassination.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/objectives/assassination.lua) | 暗杀目标系统 |
| [brigaspawn.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/objectives/brigaspawn.lua) | Brigador生成目标 |
| [omegassassination.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/objectives/omegassassination.lua) | Omega暗杀目标 |

---

## 八、工具库 (assets/scripts/include/)

| 文件 | 作用 |
|------|------|
| [csv.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/include/csv.lua) | CSV文件解析库 |
| [uuid.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/include/uuid.lua) | UUID生成库 |
| [bindingstubs.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/include/bindingstubs.lua) | 绑定存根 |

---

## 九、数据和辅助 (assets/scripts/data/ 与 assets/scripts/helper/)

| 文件 | 作用 |
|------|------|
| [data/predicates](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/data/predicates) | 谓词定义（目录） |
| [data/predicates.bak](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/data/predicates.bak) | 谓词定义备份 |
| [data/campaign_saves/placeholder.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/data/campaign_saves/placeholder.lua) | 战役存档占位符 |
| [helper/zombiedebug.lua](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/helper/zombiedebug.lua) | 僵尸调试脚本 |

---

## 十、物品栏定义 (assets/scripts/inventory/)

| 文件 | 作用 |
|------|------|
| [inventory/null.json](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/inventory/null.json) | 空物品定义 |
| [inventory/test.json](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/assets/scripts/inventory/test.json) | 测试物品定义 |

---

## 统计汇总

| 类别 | 数量 |
|------|------|
| 根目录脚本 | 5 |
| 核心库 (lib) | 16 |
| Monads系统 | 30 |
| 关卡对象 | 38 |
| 关卡工具箱 | 14 |
| 关卡脚本 | 12 |
| 目标系统 | 3 |
| 工具库 | 3 |
| **总计（Lua脚本）** | **117** |

---

## 架构说明

Brigador Killers Demo 的脚本系统采用模块化设计，主要分为以下几个层次：

1. **核心库层 (lib/)**：提供基础功能，包括工具函数、回调、碰撞检测、对话系统等
2. **Monads层**：实现函数式动作链编程，用于构建复杂的游戏事件流程
3. **对象层 (level_objects/)**：定义可交互的游戏对象
4. **工具层 (level_toolkit/)**：提供关卡设计和事件处理的实用工具
5. **关卡层 (level_scripts/)**：包含具体关卡的剧情和任务逻辑

这种设计使得游戏逻辑可以灵活组合和重用，便于关卡设计和剧情开发。

---

## 文件位置

本文档位于：[lua脚本目录.md](file:///c:/Program%20Files%20(x86)/Steam/steamapps/common/Brigador%20Killers%20Demo/lua脚本目录.md)
