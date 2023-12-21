// profile.js

import React from 'react';
import { render } from 'react-dom';

const Profile = () => {
    const userInfoJson = document.getElementById('profile').dataset.userInfo;
    const userInfo = JSON.parse(userInfoJson);

    return (
        <div>
            <h1>User Profile</h1>
            <p>Username: {userInfo.username}</p>
            {userInfo.email &&<p>Email: {userInfo.email}</p>}
            {userInfo.avatar && <img src={userInfo.avatar} alt="Avatar" />} 
            <p>Nickname: {userInfo.nickname}</p>
            {/* Add more user information as needed */}
        </div>
    );
};

const profileDiv = document.getElementById('profile');
if (profileDiv) {
    render(<Profile />, profileDiv);
}
