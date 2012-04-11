module Counter {
  interface R {
    idempotent int get();
  };
  interface W {
    ["freeze:write"] void set(int value);
    ["freeze:write"] void inc();
  };

  class RWPersistent implements R, W {
    int status;
  };
};
