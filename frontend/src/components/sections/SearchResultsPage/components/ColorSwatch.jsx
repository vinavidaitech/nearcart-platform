// components/sections/SearchResultsPage/components/ColorSwatch.jsx
export default function ColorSwatch({ color }) {
  return (
    <div
      className="w-4 h-4 rounded-full shrink-0 border border-black/10"
      style={{ background: color }}
    />
  );
}
