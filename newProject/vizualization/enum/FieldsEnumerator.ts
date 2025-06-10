
enum Fields  {
  AU = 'Authors',
  DE = 'Keywords', 
  CR = 'Cited References',
  PY = 'Publication Year',
  TI = 'Title',
  AB = 'Abstract'
}

export default class FrequencyFields {
  public static readonly FIELDS = Fields;
  public static readonly KEYS: any;
  public static readonly LABELS?: any;
  public static hasKey(key: string): boolean {
    return Object.keys(this.KEYS).includes(key);
  }
}

