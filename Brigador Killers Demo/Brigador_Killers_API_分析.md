# Brigador Killers Demo 游戏对象、数据结构和函数清单

## 目录
1. [AI状态枚举 (AISTATE)](#ai状态枚举-aistate)
2. [行为枚举 (BEHAVIOR)](#行为枚举-behavior)
3. [资源类型枚举 (RESOURCE_TYPE)](#资源类型枚举-resource_type)
4. [团队枚举 (TEAMS)](#团队枚举-teams)
5. [文本对齐枚举 (TEXT_ALIGN)](#文本对齐枚举-text_align)
6. [输入状态枚举 (INPUT_STATUS)](#输入状态枚举-input_status)
7. [图形/绘图相关](#图形绘图相关)
8. [游戏对象类](#游戏对象类)
9. [游戏逻辑/控制函数](#游戏逻辑控制函数)
10. [谓词系统](#谓词系统)
11. [全局变量表 (_gvar)](#全局变量表-_gvar)
12. [任务变量表 (_mvar)](#任务变量表-_mvar)
13. [Lua标准库扩展](#lua标准库扩展)

---

## AI状态枚举 (AISTATE)

| 名称 | 值 | 说明 |
|------|-----|------|
| PLAYER | 0 | 玩家控制 |
| AMBUSH | 1 | 伏击 |
| GOTO_LAST_KNOWN | 2 | 前往最后已知位置 |
| FLEE | 4 | 逃跑 |
| IDLE | 5 | 待机 |
| STATIONARY_SHOOT | 6 | 原地射击 |
| RETREAT | 7 | 撤退 |
| STUNNED | 8 | 眩晕 |
| FLANK | 9 | 侧翼包抄 |
| NORMAL_GOTO_FIRING_POSITION | 14 | 常规：前往射击位置 |
| NORMAL_SHOOT_TARGET | 15 | 常规：射击目标 |
| NORMAL_INVESTIGATE_POSITION | 16 | 常规：调查位置 |
| FLATFOOTED | 17 | 无防备状态 |
| BIKEJOUST_JOUST | 18 | 摩托车对撞 |
| SERPENTINE_GOTO_FIRING_POSITION | 19 | 蛇形：前往射击位置 |
| SERPENTINE_GOTO_FIRING_POSITION_ZIG | 20 | 蛇形：前往射击位置（之字形） |
| SERPENTINE_GOTO_FIRING_POSITION_ZAG | 21 | 蛇形：前往射击位置（反之字形） |
| SERPENTINE_SHOOT_TARGET | 22 | 蛇形：射击目标 |
| SERPENTINE_SHOOT_TARGET_ZIG | 23 | 蛇形：射击目标（之字形） |
| SERPENTINE_SHOOT_TARGET_ZAG | 24 | 蛇形：射击目标（反之字形） |
| SERPENTINE_INVESTIGATE_POSITION | 25 | 蛇形：调查位置 |
| WAITING | 13 | 等待 |
| ORDERED_DELAY | 12 | 命令延迟 |
| ORDER_GETIN | 11 | 命令：进入 |
| ORDER_MOVETO | 10 | 命令：移动到 |
| AISTATE_DELAYED_NEXT_STATE_OVERRIDE_BUG0 | 26 | 延迟下一个状态覆盖bug0 |
| AISTATE_DELAYED_NEXT_STATE_OVERRIDE_BUG1 | 27 | 延迟下一个状态覆盖bug1 |
| AISTATE_NULL | 28 | 空AI状态 |
| AISTATE_PLACEHOLDER | 29 | 占位符AI状态 |

---

## 行为枚举 (BEHAVIOR)

| 名称 | 值 | 说明 |
|------|-----|------|
| BEHAVIOR_PLAYER | 0 | 玩家行为 |
| BEHAVIOR_NORMAL | 1 | 常规行为 |
| BEHAVIOR_BIKEJOUST | 2 | 摩托车对撞行为 |
| BEHAVIOR_SERPENTINE | 3 | 蛇形行为 |
| BEHAVIOR_CIVILIAN | 4 | 平民行为 |
| BEHAVIOR_TANKDESTROYER | 5 | 坦克歼击车行为 |
| BEHAVIOR_INFANTRY_AIMSHOOT | 6 | 步兵瞄准射击行为 |
| BEHAVIOR_WAIT | 7 | 等待行为 |
| BEHAVIOR_NULL | 8 | 空行为 |
| BEHAVIOR_DELAYED_NEXT_STATE_OVERRIDE_BUG | 9 | 延迟下一个状态覆盖bug |

---

## 资源类型枚举 (RESOURCE_TYPE)

| 名称 | 值 | 说明 |
|------|-----|------|
| RESOURCE_RAW | 0 | 原始资源 |
| RESOURCE_SPRITE | 1 | 精灵 |
| RESOURCE_BULLET | 2 | 子弹 |
| RESOURCE_EXPLOSIVE_BULLET | 3 | 爆炸子弹 |
| RESOURCE_FLAME_BULLET | 4 | 火焰子弹 |
| RESOURCE_SMOKE_BULLET | 5 | 烟雾子弹 |
| RESOURCE_EMP_BULLET | 6 | EMP子弹 |
| RESOURCE_PROJECTILE_WEAPON | 7 | 投射武器 |
| RESOURCE_ARTILLERY_WEAPON | 8 | 火炮武器 |
| RESOURCE_LASER_WEAPON | 9 | 激光武器 |
| RESOURCE_HORN_WEAPON | 10 | 喇叭武器 |
| RESOURCE_LEG | 11 | 腿 |
| RESOURCE_CHASSIS | 12 | 底盘 |
| RESOURCE_HULL | 13 | 船体 |
| RESOURCE_MECH | 14 | 机甲 |
| RESOURCE_MATERIAL | 15 | 材质 |
| RESOURCE_WEAPON_EFFECTS | 16 | 武器特效 |
| RESOURCE_GANG | 17 | 帮派 |
| RESOURCE_GIB | 18 | 碎块 |
| RESOURCE_PYRO | 19 | 火焰 |
| RESOURCE_ARMOR_PICKUP | 20 | 护甲拾取物 |
| RESOURCE_SALVAGE | 21 | 战利品 |
| RESOURCE_TRAMPLE | 22 | 践踏 |
| RESOURCE_LIGHT | 23 | 灯光 |
| RESOURCE_EASING | 24 | 缓动 |
| RESOURCE_PROP | 25 | 道具 |
| RESOURCE_EXPLOSIVE_PROP | 26 | 爆炸道具 |
| RESOURCE_AMMO_DEPOT_PROP | 27 | 弹药库道具 |
| RESOURCE_SCENERY | 28 | 风景 |
| RESOURCE_LIGHTING | 29 | 光照 |
| RESOURCE_GLOBAL | 30 | 全局 |
| RESOURCE_ACTIVATION | 31 | 激活 |
| RESOURCE_TRAP | 32 | 陷阱 |
| RESOURCE_ABILITY | 33 | 能力 |
| RESOURCE_MECHABILITY | 34 | 机甲能力 |
| RESOURCE_TANKABILITY | 35 | 坦克能力 |
| RESOURCE_POWINF_ABILITY | 36 | 步兵能力 |
| RESOURCE_HOVERABILITY | 37 | 悬浮能力 |
| RESOURCE_LEVEL_EXIT | 38 | 关卡出口 |
| RESOURCE_MOUSE_CURSOR | 39 | 鼠标光标 |
| RESOURCE_GATE | 40 | 门 |
| RESOURCE_EMP_ABILITY | 41 | EMP能力 |
| RESOURCE_SILENT_RUN_ABILITY | 42 | 静音运行能力 |
| RESOURCE_GUN_ABILITY | 43 | 枪械能力 |
| RESOURCE_RUBBLE | 44 | 瓦砾 |
| RESOURCE_RUBBLE_LIST | 45 | 瓦砾列表 |
| RESOURCE_OVERMAP | 46 | 大地图 |
| RESOURCE_MISSION | 47 | 任务 |
| RESOURCE_TURRET_PROP | 48 | 炮塔道具 |
| RESOURCE_DOOR_PROP | 49 | 门道具 |
| RESOURCE_SUBSTATION_PROP | 50 | 变电站道具 |
| RESOURCE_COMM_STATION_PROP | 51 | 通讯站道具 |
| RESOURCE_PILOT | 52 | 驾驶员 |
| RESOURCE_INTEL | 53 | 情报 |
| RESOURCE_COMPRESSED_IMAGE | 54 | 压缩图像 |
| RESOURCE_FIDELIS | 55 | Fidelis |
| RESOURCE_MECH_LOADOUT | 56 | 机甲装备 |
| RESOURCE_COMBAT_VARS | 57 | 战斗变量 |
| RESOURCE_MOD_APPENDAGE | 58 | 附属物修改 |
| RESOURCE_STAT_MODIFIER | 59 | 属性修改器 |
| RESOURCE_DIALOGUE_THEME | 60 | 对话主题 |
| RESOURCE_ITEM_PICKUP | 61 | 物品拾取物 |
| RESOURCE_PLAYLIST | 62 | 播放列表 |
| RESOURCE_AMBIENTEMITTER | 63 | 环境发射器 |
| RESOURCE_RECIPE | 64 | 配方 |
| RESOURCE_ITEM_EXPLOSIVE | 65 | 物品爆炸物 |

---

## 团队枚举 (TEAMS)

| 名称 | 值 | 说明 |
|------|-----|------|
| PLAYER_TEAM | 0 | 玩家团队 |
| ENEMY_TEAM | 1 | 敌人团队 |
| CIVILIAN_TEAM | 2 | 平民团队 |

---

## 文本对齐枚举 (TEXT_ALIGN)

| 名称 | 值 | 说明 |
|------|-----|------|
| LEFT | 0 | 左对齐 |
| CENTER | 1 | 居中对齐 |
| RIGHT | 2 | 右对齐 |

---

## 输入状态枚举 (INPUT_STATUS)

| 名称 | 值 | 说明 |
|------|-----|------|
| DOWN | 1 | 按下 |
| MINUS | 2 | 减少 |
| PLUS | 3 | 增加 |

---

## 图形/绘图相关

### Canvas 表
| 函数 | 说明 |
|------|------|
| DrawCRT | 绘制CRT效果 |
| DrawPolygon | 绘制多边形 |
| DrawRectangle | 绘制矩形 |
| DrawText | 绘制文本 |
| DrawTextAlign | 绘制对齐文本 |
| FontMetrics | 获取字体度量 |
| GetEmScaling | 获取Em缩放 |
| GetLineSpacing | 获取行间距 |
| PopClip | 弹出裁剪 |
| PushClip | 推入裁剪 |
| ToScreen | 转换到屏幕坐标 |

### Color 表
| 函数 | 说明 |
|------|------|
| New | 创建新颜色 |

### Rect2 表
| 函数 | 说明 |
|------|------|
| New | 创建新矩形 |

### Screen 表
| 函数 | 说明 |
|------|------|
| DrawRectangle | 绘制矩形到屏幕 |
| DrawText | 绘制文本到屏幕 |
| DrawTextOutlined | 绘制带轮廓文本到屏幕 |
| FromWorld | 从世界坐标转换 |
| GetLineSpacing | 获取行间距 |
| PopClip | 弹出裁剪 |
| PushClip | 推入裁剪 |
| ToCanvas | 转换到画布 |

### Sprite 表
| 函数 | 说明 |
|------|------|
| New | 创建新精灵 |

### Texture 表
| 函数 | 说明 |
|------|------|
| New | 创建新纹理 |

### Vec2 表
| 函数 | 说明 |
|------|------|
| New | 创建新二维向量 |

### World 表
| 函数 | 说明 |
|------|------|
| DrawLine | 在世界中绘制线 |
| DrawRectangle | 在世界中绘制矩形 |
| DrawText | 在世界中绘制文本 |

---

## 游戏对象类

### FastMech 表
| 函数 | 说明 |
|------|------|
| New | 创建快速机甲 |

### Mech 表
| 函数 | 说明 |
|------|------|
| Create | 创建机甲 |
| GetPlayer | 获取玩家机甲 |
| GetPlayerHovered | 获取玩家悬停的机甲 |
| New | 创建新机甲 |

### Gun 表
| 说明 | 枪械表 |
|------|--------|

---

## 游戏逻辑/控制函数

### 任务/目标系统
| 函数 | 说明 |
|------|------|
| register_objective | 注册目标 |
| complete_objective | 完成目标 |
| fail_objective | 失败目标 |

### 游戏流程控制
| 函数 | 说明 |
|------|------|
| win | 胜利 |
| defeat | 失败 |
| MissionWin | 任务胜利 |
| MissionFail | 任务失败 |
| FadeToBlack | 淡入到黑色 |
| reset_character | 重置角色 |
| set_character | 设置角色 |

### 回调注册
| 函数 | 说明 |
|------|------|
| register_init_function | 注册初始化函数 |
| register_update_function | 注册更新函数 |
| register_draw_function | 注册绘制函数 |
| register_levelexit_function | 注册关卡退出函数 |
| register_defeat_function | 注册失败函数 |
| register_win_function | 注册胜利函数 |

### 对话框系统
| 函数 | 说明 |
|------|------|
| request_next_dialogue_action | 请求下一个对话动作 |
| did_next_dialogue_action | 下一个对话动作已完成 |

### 资源系统
| 函数 | 说明 |
|------|------|
| resource_unlocked | 检查资源是否已解锁 |
| unlock_resource | 解锁资源 |
| write_back_resource | 回写资源 |

### 存档/配置
| 函数 | 说明 |
|------|------|
| save_profile | 保存档案 |
| set_hub | 设置枢纽 |
| set_mission | 设置任务 |

### 控制台
| 函数 | 说明 |
|------|------|
| OpenConsole | 打开控制台 |
| set_console_disabled | 设置控制台禁用 |
| set_console_hidden | 设置控制台隐藏 |
| set_console_prompt | 设置控制台提示 |
| set_console_sprite | 设置控制台精灵 |
| create_uiconsole | 创建UI控制台 |

### 门系统
| 函数 | 说明 |
|------|------|
| set_door_state | 设置门状态 |

### 音效/音乐
| 函数 | 说明 |
|------|------|
| play | 播放 |
| pause | 暂停 |
| unpause | 取消暂停 |
| unpause_play | 取消暂停并播放 |
| PlaySound | 播放音效 |
| SetMusic | 设置音乐 |

### 世界创建
| 函数 | 说明 |
|------|------|
| create_explosive | 创建爆炸物 |
| create_pickup | 创建拾取物 |
| create_scenery | 创建风景 |
| create_rangefinder | 创建测距仪 |
| create_mission_selector | 创建任务选择器 |

### 物品系统
| 函数 | 说明 |
|------|------|
| GunPickup | 枪械拾取 |
| UnlockItem | 解锁物品 |
| UnlockWeapon | 解锁武器 |
| UnlockVehicle | 解锁载具 |
| UnlockTape | 解锁磁带 |
| add_usable_item | 添加可用物品 |
| HandleItemUnlock | 处理物品解锁 |

### 全局变量操作
| 函数 | 说明 |
|------|------|
| SetGvar0 | 设置全局变量0 |
| SetGvar1 | 设置全局变量1 |
| SetGvar2 | 设置全局变量2 |
| SetGvar3 | 设置全局变量3 |
| SetGvar4 | 设置全局变量4 |
| SetGvar5 | 设置全局变量5 |
| SetTrue | 设置为真 |
| SetFalse | 设置为假 |
| DefaultTrue | 默认真 |
| IncrementGvar | 增加全局变量 |
| DecrementGvar | 减少全局变量 |
| MergeGvars | 合并全局变量 |
| PrintGvars | 打印全局变量 |
| PrintPredicates | 打印谓词 |

### 位置标记
| 函数 | 说明 |
|------|------|
| queue_location_marker | 队列位置标记 |

### 杂项
| 函数 | 说明 |
|------|------|
| AppendToHistory | 追加到历史记录 |
| DelayedAction | 延迟动作 |
| Hughjection | Hughjection |
| HughjectionGeneric | 通用Hughjection |
| IdleMech | 待机甲 |
| KeyItemCallback | 关键物品回调 |
| KeyItemIncrementCallback | 关键物品增加回调 |
| KeyItemSetToFive | 关键物品设置为5 |
| ExtractMechName | 提取机甲名称 |
| extract | 提取 |
| SetAllowEntryOff | 关闭允许进入 |
| SetAllowEntryOn | 开启允许进入 |
| ToggleAllowEntry | 切换允许进入 |
| SetCivvieJean | 设置平民Jean |
| SetFortFab | 设置FortFab |
| SpawnMechDialogueEnd | 生成机甲对话结束 |
| change_player_base | 改变玩家基础 |
| cmd | 命令 |
| StringStartsWith | 字符串开头检查 |
| TableShallowCopy | 表浅拷贝 |
| TableToString | 表转字符串 |
| ResetLoadedScripts | 重置已加载脚本 |
| DealerDied | 商人死亡 |

---

## 谓词系统

### __predicate_definition 表
包含谓词定义，格式为字符串表达式。

### __predicates 表
包含谓词函数，可执行条件判断。

#### 常用谓词
| 谓词名 | 说明（推测） |
|--------|-------------|
| always_true | 总是为真 |
| always_false | 总是为假 |
| in_hub | 在枢纽中 |
| in_mission | 在任务中 |
| in_newgame | 在新游戏中 |
| is_barclaw_intro | 是Barclay介绍 |
| vehicle_entry_enabled | 载具进入已启用 |
| johnny | Johnny |
| johnny_guitar | Johnny和吉他 |
| keybroker_intronottriggered | 钥匙经纪人介绍未触发 |
| keybroker_hasntgiven_key | 钥匙经纪人未给钥匙 |
| keybroker_is_killed | 钥匙经纪人被杀死 |
| keybroker_key_drop | 钥匙经纪人钥匙掉落 |
| meeting_mendac_peaceful | 和平会见Mendac |
| mendac_empty_handed | Mendac空手 |
| met_mendac_at_all | 已会见Mendac |
| metfoal_beenseen | Metfoal已被看到 |
| metfoal_notseen | Metfoal未被看到 |
| pipes_intro_unseen | 管道介绍未看到 |
| first_tape_delivered | 第一盘磁带已交付 |
| repeat_brief_tapes_prompt | 重复简短磁带提示 |
| repeatedly_emptyhanded | 反复空手 |
| shot_stranger_mendac | 向陌生人Mendac开枪 |
| toolkit_show | 显示工具箱 |
| dev_explainer_notmet | 开发者说明未遇到 |
| dungeon_floor_0-4, final, not_final | 地牢楼层 |
| e01_h00_m01 及相关 | Holger公寓任务相关 |
| e01_h02_* | 军械库任务相关 |
| e01_has_* | 拥有某载具/物品 |
| hideout_* | 藏身处相关 |
| hideout_mastertoggle_active | 藏身处主开关激活 |
| zzz_assembler_* | 组装机相关 |
| zzz_hundo_firstmeet | Hundo第一次见面 |
| zzz_swatgate_is_down/up | SWAT门状态 |
| c01_h00_* | 关卡1相关 |
| carmine_* | Carmine相关 |
| chob_* | Chob相关 |

---

## 全局变量表 (_gvar)

| 变量名 | 类型 | 默认值 | 说明（推测） |
|--------|------|--------|-------------|
| bktest_dungeon_console | number | 0 | 测试地牢控制台 |
| c01_h00_bulver_speaks | boolean | true | Bulver说话 |
| c01_h00_intro_completedintro | boolean | false | 介绍已完成 |
| c01_h00_killed_archer | boolean | false | 杀死Archer |
| c01_h00_killed_bulver | boolean | false | 杀死Bulver |
| c01_h00_killed_ka | boolean | false | 杀死Ka |
| c01_h00_killed_wrightson | boolean | false | 杀死Wrightson |
| chob_always_false | boolean | false | Chob总是假 |
| chob_always_true | boolean | true | Chob总是真 |
| chob_gantry_state | boolean | false | Chob龙门架状态 |
| chob_state_4 | boolean | false | Chob状态4 |
| chob_state_A | number | 0 | Chob状态A |
| chob_string | string | "nothing" | Chob字符串 |
| dev_explainer_met | boolean | false | 已遇到开发者说明 |
| dungeon_floor | number | 0 | 地牢楼层 |
| e01_h00_m01_i_bathroomcleaned | boolean | false | 浴室已清洁 |
| e01_h00_m01_i_bathroomneedscleaning | boolean | false | 浴室需要清洁 |
| e01_h00_m01_i_coplights | boolean | false | 警察灯 |
| e01_h00_m01_i_haswad | boolean | false | 有包裹 |
| e01_h00_m01_i_joveintroduced | boolean | false | Jove已介绍 |
| e01_h00_m01_m_collider | boolean | false | 碰撞体 |
| e01_h00_m01_m_hasmoney | boolean | false | 有钱 |
| e01_h00_m01_m_holgerburnid | boolean | false | Holger烧ID |
| e01_h00_m01_m_jovefound | boolean | false | Jove已找到 |
| e01_h00_m01_m_jovemounted | boolean | false | Jove已上车 |
| e01_h00_m01_m_needmoney | boolean | false | 需要钱 |
| e01_h00_m01_m_parkedathospital | boolean | false | 停在医院 |
| e01_h00_m01_m_spoketolilrn | boolean | false | 和Lilrn说话 |
| e01_h00_m01_o_playerdied | boolean | false | 玩家死亡 |
| e01_h02_gantrystatus | number | 5 | 龙门架状态 |
| e01_h02_m00_dead_corvids | number | 5 | 死亡的Corvids数量 |
| e01_h02_m00_hint_disabled | boolean | false | 提示已禁用 |
| e01_h02_should_tutorialize | boolean | true | 应该教程化 |
| e01_h02_t_armory | boolean | false | 军械库 |
| e01_h02_t_exit | boolean | true | 出口 |
| e01_h02_t_gantry | boolean | false | 龙门架 |
| e01_h02_t_mission | boolean | false | 任务 |
| e01_has_carmine | boolean | true | 拥有Carmine |
| e01_has_cinderblock | boolean | true | 拥有Cinderblock |
| e01_has_dromon | boolean | true | 拥有Dromon |
| e01_has_faber | boolean | false | 拥有Faber |
| e01_has_loyalist | boolean | true | 拥有Loyalist |
| e01_has_swat | boolean | false | 拥有SWAT |
| hideout_carmine_01 | boolean | false | 藏身处Carmine 01 |
| hideout_guns_01-05 | boolean | false | 藏身处枪械 |
| hideout_guns_starter | boolean | false | 藏身处初始枪械 |
| hideout_mastertoggle | boolean | false | 藏身处主开关 |
| hideout_vics | number | 0 | 藏身处受害者 |
| metfoal_intro_beenseen | boolean | false | Metfoal介绍已看到 |
| test_gvar | boolean | false | 测试全局变量 |
| toolkit_bool | boolean | false | 工具箱布尔值 |
| toolkit_number | number | 0 | 工具箱数值 |
| toolkit_string | string | "nothing" | 工具箱字符串 |
| zzz_assembler_haspower | boolean | false | 组装机有电源 |
| zzz_assembler_needsintro | boolean | true | 组装机需要介绍 |
| zzz_assembler_parts_carmine | number | 2 | 组装机Carmine零件 |
| zzz_assembler_parts_fork | number | 1 | 组装机Fork零件 |
| zzz_assembler_parts_wheelchair | number | 5 | 组装机轮椅零件 |
| zzz_assembler_target | string | "none" | 组装机目标 |
| zzz_assembler_used | number | 0 | 组装机使用次数 |
| zzz_hundo_firstconvo | boolean | true | Hundo第一次对话 |
| zzz_number | number | 0 | Zzz数值 |
| zzz_string | string | "zzz test string" | Zzz字符串 |
| zzz_swatgate_up | boolean | true | SWAT门升起 |
| zzz_toggle | boolean | false | Zzz开关 |

---

## 任务变量表 (_mvar)

| 变量名 | 类型 | 默认值 | 说明（推测） |
|--------|------|--------|-------------|
| campaign_state | string | "HUB" | 战役状态 |
| dialogue_depth | number | 0 | 对话深度 |
| spawned_loadout | table | - | 生成的装备 |
| spawned_vehicle | string | "" | 生成的载具 |

---

## Lua标准库扩展

### 标准库函数
- assert
- error
- ipairs
- pairs
- pcall
- xpcall
- type
- tonumber
- tostring
- select
- next
- rawequal
- rawget
- rawset
- setmetatable
- getmetatable
- setfenv
- getfenv
- unpack
- require
- dofile
- load
- loadfile
- loadstring
- print
- collectgarbage
- time

### 扩展的table库
- table.clear: 清空表
- table.clone: 克隆表
- table.isarray: 检查是否为数组
- table.isempty: 检查是否为空
- table.new: 创建新表
- table.nkeys: 获取键的数量

### 扩展的string库
- string.buffer: 字符串缓冲区

### 扩展的其他功能
- jit.util: JIT工具
- searchpath: 搜索路径
- seeall: 查看全部

---

## 总结

这是Brigador Killers Demo游戏的完整Lua环境分析，包含：
- 完整的AI状态、行为、资源类型等枚举
- 图形/绘图API
- 游戏对象类（机甲、枪械等）
- 丰富的游戏控制函数
- 强大的谓词系统用于剧情分支
- 完整的全局变量和任务变量系统
- 扩展的Lua标准库

这个游戏似乎是一个机甲战斗游戏，带有任务系统、剧情分支、载具解锁、武器系统等功能。
