import Link from "next/link";
import { CATEGORIES } from "@/lib/plugins";

interface CategoryFilterProps {
  selectedCategory?: string;
}

export default function CategoryFilter({ selectedCategory }: CategoryFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <Link
        href="/plugins"
        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
          !selectedCategory
            ? "bg-purple-600 text-white"
            : "bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700"
        }`}
      >
        全部
      </Link>
      {CATEGORIES.map((cat) => (
        <Link
          key={cat.id}
          href={`/plugins?category=${cat.id}`}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
            selectedCategory === cat.id
              ? "bg-purple-600 text-white"
              : "bg-gray-800 text-gray-300 hover:bg-gray-700 border border-gray-700"
          }`}
        >
          <span>{cat.icon}</span>
          <span>{cat.label}</span>
        </Link>
      ))}
    </div>
  );
}
