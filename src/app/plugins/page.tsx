import { searchPlugins, CATEGORIES } from "@/lib/plugins";
import type { Category } from "@/lib/plugins";
import PluginCard from "@/components/PluginCard";
import CategoryFilter from "@/components/CategoryFilter";

interface PluginsPageProps {
  searchParams: Promise<{ category?: string; q?: string }>;
}

export default async function PluginsPage({ searchParams }: PluginsPageProps) {
  const params = await searchParams;
  const category = params.category as Category | undefined;
  const query = params.q ?? "";

  const plugins = searchPlugins(query, category);
  const catInfo = category ? CATEGORIES.find((c) => c.id === category) : undefined;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">
          {catInfo ? (
            <span className="flex items-center gap-2">
              <span>{catInfo.icon}</span>
              <span>{catInfo.label}</span>
            </span>
          ) : (
            "所有插件"
          )}
        </h1>
        {catInfo && (
          <p className="text-gray-400">{catInfo.description}</p>
        )}
        <p className="text-gray-500 text-sm mt-2">共 {plugins.length} 款插件</p>
      </div>

      {/* Category Filter */}
      <div className="mb-8 overflow-x-auto">
        <CategoryFilter selectedCategory={category} />
      </div>

      {/* Plugin Grid */}
      {plugins.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {plugins.map((plugin) => (
            <PluginCard key={plugin.id} plugin={plugin} featured={plugin.featured} />
          ))}
        </div>
      ) : (
        <div className="text-center py-24 text-gray-500">
          <div className="text-5xl mb-4">🔍</div>
          <p className="text-lg">未找到匹配的插件</p>
          <p className="text-sm mt-2">尝试换一个搜索词或选择其他分类</p>
        </div>
      )}
    </div>
  );
}
