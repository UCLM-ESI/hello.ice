module Services {
  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ObjectPrxDict;

  interface NestedContainer {
    void link(string key, Object* proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    Object* get(string key) throws NoSuchKey;
    ObjectPrxDict list();
    Container* makeContainer(string key);
  };
};
