export class PaginatedResponse<T> {
  total: number;
  page: number;
  perPage: number;
  items: T[];

  constructor(data: Partial<PaginatedResponse<T>>) {
    this.total = data.total ?? 0;
    this.page = data.page ?? 1;
    this.perPage = data.perPage ?? 10;
    this.items = data.items ?? [];
  }

  get nextPage(): number | undefined {
    const { total, page, perPage, items } = this;

    return (page - 1) * perPage + items.length >= total ? undefined : page + 1;
  }
}
