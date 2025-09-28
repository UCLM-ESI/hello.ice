module Armory {
  interface PanTilt {
    void down();
    void up();
    void left();
    void right();
    void stop();
    void fire();
  };

  exception InvalidToken {
    string message;
  };

  interface TurretFactory {
    PanTilt* getPanTilt(int token) throws InvalidToken;
  };
};
