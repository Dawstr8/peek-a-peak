import SummitProgress from "./components/summit-progress";

export default function DiaryPage() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <SummitProgress />
    </div>
  );
}
