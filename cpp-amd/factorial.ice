module Example {

  exception RequestCanceledException {};

  interface Math {
    ["amd"] long factorial(int value);
  };
};
