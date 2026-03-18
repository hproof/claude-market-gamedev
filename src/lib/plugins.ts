export type Category =
  | "game-engine"
  | "ai-npc"
  | "procedural"
  | "asset-management"
  | "narrative"
  | "audio"
  | "physics"
  | "multiplayer"
  | "analytics"
  | "testing";

export interface Plugin {
  id: string;
  name: string;
  description: string;
  longDescription: string;
  category: Category;
  author: string;
  authorAvatar: string;
  version: string;
  downloads: number;
  rating: number;
  reviewCount: number;
  tags: string[];
  price: "free" | number;
  featured: boolean;
  updatedAt: string;
  icon: string;
  screenshots: string[];
  features: string[];
  requirements: string[];
  changelog: { version: string; date: string; notes: string }[];
}

export const CATEGORIES: { id: Category; label: string; icon: string; description: string }[] = [
  {
    id: "game-engine",
    label: "游戏引擎集成",
    icon: "🎮",
    description: "Unity、Unreal、Godot 等引擎的 Claude AI 集成插件",
  },
  {
    id: "ai-npc",
    label: "AI NPC 对话",
    icon: "🤖",
    description: "让游戏 NPC 具备智能对话能力",
  },
  {
    id: "procedural",
    label: "程序化生成",
    icon: "🌍",
    description: "利用 AI 生成关卡、地图、道具等游戏内容",
  },
  {
    id: "asset-management",
    label: "资产管理",
    icon: "📦",
    description: "智能管理游戏素材、纹理、模型等资源",
  },
  {
    id: "narrative",
    label: "叙事与剧情",
    icon: "📖",
    description: "AI 辅助生成游戏剧情、对话和任务文本",
  },
  {
    id: "audio",
    label: "音频生成",
    icon: "🎵",
    description: "利用 AI 生成游戏音效、背景音乐和语音",
  },
  {
    id: "physics",
    label: "物理模拟",
    icon: "⚛️",
    description: "AI 增强的物理引擎与模拟工具",
  },
  {
    id: "multiplayer",
    label: "多人联机",
    icon: "🌐",
    description: "智能匹配、反作弊与多人游戏体验优化",
  },
  {
    id: "analytics",
    label: "游戏分析",
    icon: "📊",
    description: "玩家行为分析、留存优化与数据洞察",
  },
  {
    id: "testing",
    label: "自动化测试",
    icon: "🧪",
    description: "AI 驱动的游戏测试、bug 发现与质量保障",
  },
];

export const PLUGINS: Plugin[] = [
  {
    id: "unity-claude-bridge",
    name: "Unity Claude Bridge",
    description: "在 Unity 编辑器中直接调用 Claude API，支持代码生成、资产描述与 AI 辅助调试。",
    longDescription:
      "Unity Claude Bridge 是一款功能强大的 Unity 编辑器插件，将 Anthropic Claude 的 AI 能力无缝嵌入到您的游戏开发工作流中。\n\n通过此插件，您可以在编辑器内直接向 Claude 提问、生成脚本、分析 bug、生成资产描述，大幅提升开发效率。支持 Unity 2021.3 LTS 及以上版本，兼容 URP 和 HDRP 渲染管线。",
    category: "game-engine",
    author: "GameAI Studio",
    authorAvatar: "GA",
    version: "2.3.1",
    downloads: 48200,
    rating: 4.8,
    reviewCount: 312,
    tags: ["Unity", "C#", "代码生成", "调试", "AI助手"],
    price: "free",
    featured: true,
    updatedAt: "2026-03-10",
    icon: "🎮",
    screenshots: [],
    features: [
      "在 Unity 编辑器内嵌 Claude 对话面板",
      "一键生成 MonoBehaviour 脚本",
      "智能 Bug 分析与修复建议",
      "资产元数据自动生成",
      "支持多语言（中文/英文）",
    ],
    requirements: ["Unity 2021.3 LTS+", "Claude API Key", ".NET Standard 2.1"],
    changelog: [
      { version: "2.3.1", date: "2026-03-10", notes: "修复与 Unity 6 的兼容性问题" },
      { version: "2.3.0", date: "2026-02-20", notes: "新增代码重构建议功能" },
      { version: "2.2.0", date: "2026-01-15", notes: "支持中文界面" },
    ],
  },
  {
    id: "npc-dialogue-engine",
    name: "NPC Dialogue Engine",
    description: "基于 Claude 的动态 NPC 对话系统，让每个 NPC 拥有独特个性与记忆。",
    longDescription:
      "NPC Dialogue Engine 使用 Claude 的高级语言理解能力，为您的游戏 NPC 赋予真实的对话体验。每个 NPC 都可以设置独特的性格、背景故事和情感状态，并能记住与玩家的历史交互。\n\n支持流式输出、多轮对话、情感变化和剧情分支，完美适配 RPG、冒险和模拟类游戏。",
    category: "ai-npc",
    author: "DialogueCraft",
    authorAvatar: "DC",
    version: "1.5.0",
    downloads: 35600,
    rating: 4.9,
    reviewCount: 428,
    tags: ["NPC", "对话", "RPG", "角色扮演", "情感AI"],
    price: 29.99,
    featured: true,
    updatedAt: "2026-03-05",
    icon: "🤖",
    screenshots: [],
    features: [
      "每个 NPC 独立人格与记忆系统",
      "流式对话输出，减少等待感",
      "情感状态机（开心、愤怒、悲伤等）",
      "支持多语言本地化",
      "内置对话编辑器",
      "剧情触发钩子 API",
    ],
    requirements: ["Unity 2022.3+ 或 Unreal Engine 5.1+", "Claude API Key", "网络连接"],
    changelog: [
      { version: "1.5.0", date: "2026-03-05", notes: "新增情感状态机系统" },
      { version: "1.4.0", date: "2026-01-28", notes: "支持 Unreal Engine 5.3" },
      { version: "1.3.0", date: "2025-12-10", notes: "添加记忆持久化功能" },
    ],
  },
  {
    id: "world-forge-ai",
    name: "WorldForge AI",
    description: "使用 Claude 智能生成游戏地图、关卡布局、生态系统和世界背景故事。",
    longDescription:
      "WorldForge AI 是专为游戏设计师打造的 AI 世界生成工具。只需描述您想要的世界风格，Claude 即可生成完整的地形布局、城镇分布、NPC 居民设定和背景故事，配合可视化编辑器让世界构建变得前所未有地简单。",
    category: "procedural",
    author: "ProGenLabs",
    authorAvatar: "PG",
    version: "3.0.2",
    downloads: 22100,
    rating: 4.7,
    reviewCount: 187,
    tags: ["地图生成", "世界构建", "关卡设计", "程序化", "开放世界"],
    price: 49.99,
    featured: true,
    updatedAt: "2026-03-12",
    icon: "🌍",
    screenshots: [],
    features: [
      "自然语言描述生成地图",
      "地形、气候、生物群落自动生成",
      "城市与建筑布局智能规划",
      "世界历史与传说自动创作",
      "导出为多种格式（JSON、XML、Tiled）",
    ],
    requirements: ["Godot 4.0+ / Unity 2022.3+", "Claude API Key", "Python 3.10+"],
    changelog: [
      { version: "3.0.2", date: "2026-03-12", notes: "优化大地图生成性能" },
      { version: "3.0.0", date: "2026-02-01", notes: "全新界面与 AI 生成引擎升级" },
    ],
  },
  {
    id: "story-weaver",
    name: "StoryWeaver",
    description: "AI 驱动的游戏叙事工具，自动生成主线剧情、支线任务和动态对话树。",
    longDescription:
      "StoryWeaver 让游戏开发者能够利用 Claude 的创意写作能力，快速构建引人入胜的游戏叙事。支持分支叙事结构、玩家选择影响剧情走向、动态生成任务描述，以及与游戏事件系统的深度集成。",
    category: "narrative",
    author: "NarrativeForge",
    authorAvatar: "NF",
    version: "2.1.0",
    downloads: 18900,
    rating: 4.6,
    reviewCount: 143,
    tags: ["剧情", "任务", "对话树", "叙事", "RPG"],
    price: "free",
    featured: false,
    updatedAt: "2026-02-28",
    icon: "📖",
    screenshots: [],
    features: [
      "可视化分支剧情编辑器",
      "AI 自动填充对话内容",
      "玩家选择影响后续剧情",
      "多结局智能生成",
      "本地化翻译辅助",
    ],
    requirements: ["任意游戏引擎", "Claude API Key"],
    changelog: [
      { version: "2.1.0", date: "2026-02-28", notes: "新增多结局生成模板" },
      { version: "2.0.0", date: "2026-01-10", notes: "重构对话树编辑器" },
    ],
  },
  {
    id: "asset-tagger-pro",
    name: "AssetTagger Pro",
    description: "利用 Claude 视觉能力自动为游戏素材生成标签、描述和搜索关键词。",
    longDescription:
      "AssetTagger Pro 使用 Claude 的多模态能力，自动分析游戏美术资源（纹理、模型、动画）并生成准确的元数据标签。大幅减少手动标注工作，让资产管理更高效。",
    category: "asset-management",
    author: "AssetBot",
    authorAvatar: "AB",
    version: "1.2.3",
    downloads: 14300,
    rating: 4.5,
    reviewCount: 98,
    tags: ["资产管理", "自动标签", "元数据", "素材库"],
    price: 19.99,
    featured: false,
    updatedAt: "2026-02-15",
    icon: "📦",
    screenshots: [],
    features: [
      "批量自动标注图片/模型",
      "自定义标签分类体系",
      "与主流资产管理系统集成",
      "支持中英双语标签",
    ],
    requirements: ["Claude API Key（支持视觉）"],
    changelog: [
      { version: "1.2.3", date: "2026-02-15", notes: "提升中文标签准确率" },
      { version: "1.2.0", date: "2026-01-05", notes: "支持 3D 模型分析" },
    ],
  },
  {
    id: "soundscape-ai",
    name: "SoundScape AI",
    description: "根据游戏场景描述自动生成音效提示词，并与主流 AI 音频生成服务集成。",
    longDescription:
      "SoundScape AI 与 Claude 协同工作，分析当前游戏场景并生成精准的音效需求描述，然后自动调用 AI 音频生成服务（Suno、ElevenLabs 等）创作匹配的背景音乐和音效。",
    category: "audio",
    author: "AudioMind",
    authorAvatar: "AM",
    version: "1.0.5",
    downloads: 8700,
    rating: 4.3,
    reviewCount: 62,
    tags: ["音效", "音乐", "AI生成", "背景音乐"],
    price: 39.99,
    featured: false,
    updatedAt: "2026-02-20",
    icon: "🎵",
    screenshots: [],
    features: [
      "场景感知音效推荐",
      "自动生成音频提示词",
      "集成 Suno / ElevenLabs API",
      "音频元数据智能管理",
    ],
    requirements: ["Claude API Key", "Suno 或 ElevenLabs API Key"],
    changelog: [
      { version: "1.0.5", date: "2026-02-20", notes: "新增 ElevenLabs 音效生成支持" },
      { version: "1.0.0", date: "2026-01-20", notes: "初始发布" },
    ],
  },
  {
    id: "playtester-ai",
    name: "PlayTester AI",
    description: "AI 自动化游戏测试工具，模拟玩家行为发现 bug 和平衡性问题。",
    longDescription:
      "PlayTester AI 使用 Claude 理解游戏规则和目标，自动生成测试用例，模拟多样化的玩家行为，系统性地探索游戏状态空间并生成详细的测试报告。",
    category: "testing",
    author: "QABotLabs",
    authorAvatar: "QB",
    version: "2.0.1",
    downloads: 11200,
    rating: 4.7,
    reviewCount: 134,
    tags: ["测试", "QA", "自动化", "Bug发现", "平衡性"],
    price: "free",
    featured: true,
    updatedAt: "2026-03-08",
    icon: "🧪",
    screenshots: [],
    features: [
      "自然语言描述测试场景",
      "自动化测试脚本生成",
      "平衡性问题智能检测",
      "测试报告可视化",
      "持续集成 (CI/CD) 支持",
    ],
    requirements: ["Python 3.10+", "Claude API Key"],
    changelog: [
      { version: "2.0.1", date: "2026-03-08", notes: "修复 macOS Sequoia 兼容问题" },
      { version: "2.0.0", date: "2026-02-10", notes: "全新 AI 测试引擎" },
    ],
  },
  {
    id: "matchmaker-ai",
    name: "Matchmaker AI",
    description: "使用 Claude 分析玩家风格，实现精准的智能匹配与个性化游戏体验。",
    longDescription:
      "Matchmaker AI 通过持续分析玩家的游戏行为数据，使用 Claude 构建详细的玩家画像，实现技能水平与游戏风格的精准匹配，同时提供个性化的游戏推荐和调整建议。",
    category: "multiplayer",
    author: "NetPlay Tech",
    authorAvatar: "NT",
    version: "1.3.0",
    downloads: 9800,
    rating: 4.4,
    reviewCount: 77,
    tags: ["匹配", "多人", "玩家画像", "个性化", "竞技"],
    price: 59.99,
    featured: false,
    updatedAt: "2026-03-01",
    icon: "🌐",
    screenshots: [],
    features: [
      "玩家技能水平精准评估",
      "游戏风格智能分类",
      "动态难度自适应调整",
      "反作弊行为检测辅助",
    ],
    requirements: ["服务端 Node.js 18+", "Claude API Key", "Redis 7.0+"],
    changelog: [
      { version: "1.3.0", date: "2026-03-01", notes: "新增反作弊辅助模块" },
      { version: "1.2.0", date: "2026-01-25", notes: "优化匹配算法" },
    ],
  },
  {
    id: "retention-analyst",
    name: "Retention Analyst",
    description: "AI 分析玩家流失原因，提供数据驱动的游戏留存优化建议。",
    longDescription:
      "Retention Analyst 收集并分析玩家行为数据，利用 Claude 识别导致玩家流失的关键痛点，自动生成可落地的优化建议，帮助游戏团队提升日活跃用户数和长期留存率。",
    category: "analytics",
    author: "DataGame Inc",
    authorAvatar: "DG",
    version: "1.1.0",
    downloads: 7400,
    rating: 4.2,
    reviewCount: 51,
    tags: ["留存", "数据分析", "玩家行为", "运营", "变现"],
    price: 79.99,
    featured: false,
    updatedAt: "2026-02-25",
    icon: "📊",
    screenshots: [],
    features: [
      "玩家流失预测模型",
      "热图与行为路径分析",
      "AI 自动生成优化报告",
      "A/B 测试方案建议",
    ],
    requirements: ["Claude API Key", "数据库连接（MySQL/PostgreSQL）"],
    changelog: [
      { version: "1.1.0", date: "2026-02-25", notes: "新增 A/B 测试建议功能" },
      { version: "1.0.0", date: "2026-01-08", notes: "初始发布" },
    ],
  },
  {
    id: "unreal-claude-toolkit",
    name: "Unreal Claude Toolkit",
    description: "Unreal Engine 5 的 Claude AI 工具集，支持蓝图生成、Lumen 场景描述和 AI 辅助开发。",
    longDescription:
      "Unreal Claude Toolkit 将 Claude AI 深度集成到 Unreal Engine 5 开发工作流中，包括蓝图代码生成、材质描述、Nanite 模型优化建议和 Lumen 光照设置向导，帮助开发者更快速地实现高品质游戏画面。",
    category: "game-engine",
    author: "EpicTools Dev",
    authorAvatar: "ET",
    version: "1.8.0",
    downloads: 31500,
    rating: 4.8,
    reviewCount: 256,
    tags: ["Unreal Engine 5", "蓝图", "C++", "Lumen", "Nanite"],
    price: "free",
    featured: true,
    updatedAt: "2026-03-14",
    icon: "🎮",
    screenshots: [],
    features: [
      "蓝图节点 AI 生成向导",
      "C++ 代码补全与解释",
      "材质与着色器描述生成",
      "Lumen 光照参数优化助手",
      "资产命名规范检查",
    ],
    requirements: ["Unreal Engine 5.1+", "Claude API Key", "Visual Studio 2022"],
    changelog: [
      { version: "1.8.0", date: "2026-03-14", notes: "支持 UE 5.5 新特性" },
      { version: "1.7.0", date: "2026-02-05", notes: "新增材质生成功能" },
    ],
  },
  {
    id: "godot-claude-assistant",
    name: "Godot Claude Assistant",
    description: "Godot 4 专属 AI 助手，支持 GDScript 生成、场景设置建议和 Shader 代码辅助。",
    longDescription:
      "Godot Claude Assistant 专为 Godot 4 开发者设计，在编辑器侧边栏提供 Claude AI 交互界面，支持 GDScript 代码生成、节点配置说明、内置 Shader Language 编写辅助，以及 Godot 最佳实践建议。",
    category: "game-engine",
    author: "GodotCommunity",
    authorAvatar: "GC",
    version: "0.9.2",
    downloads: 19700,
    rating: 4.6,
    reviewCount: 168,
    tags: ["Godot 4", "GDScript", "Shader", "开源", "2D/3D"],
    price: "free",
    featured: false,
    updatedAt: "2026-03-11",
    icon: "🎮",
    screenshots: [],
    features: [
      "GDScript 智能代码生成",
      "场景节点结构建议",
      "VisualShader 辅助编写",
      "信号与事件系统向导",
    ],
    requirements: ["Godot 4.1+", "Claude API Key"],
    changelog: [
      { version: "0.9.2", date: "2026-03-11", notes: "支持 Godot 4.4" },
      { version: "0.9.0", date: "2026-02-14", notes: "Beta 版本发布" },
    ],
  },
  {
    id: "physics-tutor-ai",
    name: "PhysicsTutor AI",
    description: "AI 辅助游戏物理调试工具，自动分析异常物理行为并提供参数优化建议。",
    longDescription:
      "PhysicsTutor AI 监控游戏运行时的物理模拟数据，当检测到异常时（穿模、弹射等），自动调用 Claude 分析原因并给出具体的参数修改建议，支持 Unity Physics、Havok 和 Bullet 物理引擎。",
    category: "physics",
    author: "PhysLab",
    authorAvatar: "PL",
    version: "1.4.1",
    downloads: 6200,
    rating: 4.1,
    reviewCount: 43,
    tags: ["物理引擎", "调试", "Havok", "Bullet", "碰撞"],
    price: 24.99,
    featured: false,
    updatedAt: "2026-02-18",
    icon: "⚛️",
    screenshots: [],
    features: [
      "实时物理异常检测",
      "AI 参数优化建议",
      "支持 Unity Physics / Havok / Bullet",
      "物理日志智能分析",
    ],
    requirements: ["Unity 2022.3+ 或 Unreal Engine 5.0+", "Claude API Key"],
    changelog: [
      { version: "1.4.1", date: "2026-02-18", notes: "改进穿模检测准确率" },
      { version: "1.4.0", date: "2026-01-30", notes: "新增 Havok 支持" },
    ],
  },
];

export function getFeaturedPlugins(): Plugin[] {
  return PLUGINS.filter((p) => p.featured);
}

export function getPluginById(id: string): Plugin | undefined {
  return PLUGINS.find((p) => p.id === id);
}

export function getPluginsByCategory(category: Category): Plugin[] {
  return PLUGINS.filter((p) => p.category === category);
}

export function searchPlugins(query: string, category?: Category): Plugin[] {
  const q = query.toLowerCase();
  return PLUGINS.filter((p) => {
    const matchesCategory = !category || p.category === category;
    if (!q) return matchesCategory;
    const matchesQuery =
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some((t) => t.toLowerCase().includes(q)) ||
      p.author.toLowerCase().includes(q);
    return matchesCategory && matchesQuery;
  });
}

export function formatDownloads(n: number): string {
  if (n >= 10000) return `${(n / 10000).toFixed(1)}万`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

export function formatPrice(price: "free" | number): string {
  if (price === "free") return "免费";
  return `$${price.toFixed(2)}`;
}
