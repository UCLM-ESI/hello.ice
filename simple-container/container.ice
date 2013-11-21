module Services {
  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ProxyMap;

  interface Container {
    void link(string key, Object* proxy) throws AlreadyExists;
    void unlink(string key) throws NoSuchKey;
    ProxyMap list();
  };
};
