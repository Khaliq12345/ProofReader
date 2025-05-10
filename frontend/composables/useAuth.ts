export const useAuth = () => {
    const setLoginTime = () => {
      localStorage.setItem('login_time', new Date().toISOString());
    };
    const isLoginExpired = (): boolean => {
      const storedLoginTime = localStorage.getItem('login_time');
      if (!storedLoginTime) return true;
      const loginTime = new Date(storedLoginTime);
      const now = new Date();
      // console.log("Login : ", loginTime, " -- Now : ", now, " -- Diff (H) : ", (now.getTime() - loginTime.getTime())/3600000)
      return (now.getTime() - loginTime.getTime()) > 24 * 60 * 60 * 1000;
    };
  
    return {
      setLoginTime,
      isLoginExpired
    };
  };