// utils.js
export const getUserNickname = async (userId) => {
    try {
      const response = await fetch(`/users/getNameById/${userId}`);
      if (response.ok) {
        const data = await response.json();
        return data.nickname;
      } else {
        console.error('Error fetching user nickname:', response.status);
        return null;
      }
    } catch (error) {
      console.error('Error fetching user nickname:', error);
      return null;
    }
  };
  

export const getAvatarById = async (userId) => {
    try {
        const response = await fetch(`/api/getAvatar/${userId}`);
        if (response.ok) {
        const data = await response.json();
        return data.avatar;
        } else {
        console.error('Error fetching user nickname:', response);
        return null;
        }
    } catch (error) {
        console.error('Error fetching user nickname:', error);
        return null;
    }
    }