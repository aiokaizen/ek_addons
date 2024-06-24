self.addEventListener('push', function (event) {
    const data = event.data.json();
    const options = {
        body: data.message,
        icon: '/path/to/icon.png', // Replace with your icon path
        badge: '/path/to/badge.png' // Replace with your badge path
    };
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});
