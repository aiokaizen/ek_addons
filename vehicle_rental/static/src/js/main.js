if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/custom_module/static/src/js/service-worker.js')
        .then(function (registration) {
            console.log('Service Worker Registered', registration);
        })
        .catch(function (error) {
            console.log('Service Worker Registration Failed', error);
        });
}

function subscribeUserToPush() {
    navigator.serviceWorker.ready.then(function (registration) {
        if (!registration.pushManager) {
            console.log('Push manager unavailable.');
            return;
        }

        registration.pushManager.getSubscription().then(function (existingSubscription) {
            if (existingSubscription === null) {
                console.log('No subscription detected, making a new one.');
                registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: 'YOUR_PUBLIC_VAPID_KEY'
                }).then(function (newSubscription) {
                    console.log('New subscription added.');
                    sendSubscriptionToServer(newSubscription);
                }).catch(function (e) {
                    if (Notification.permission !== 'granted') {
                        console.log('Permission was not granted.');
                    } else {
                        console.error('An error occurred during the subscription process.', e);
                    }
                });
            } else {
                console.log('Existing subscription detected.');
                sendSubscriptionToServer(existingSubscription);
            }
        });
    });
}

function sendSubscriptionToServer(subscription) {
    // Send subscription to your server
    fetch('/save-subscription/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(subscription)
    });
}
