console.log("Sanity check!");

fetch("/accounts/config/")
.then((result) => { return result.json(); })
.then((data) => {
    const stripe = Stripe(data.publicKey);
    document.querySelector("#submitBtn").addEventListener("click", () => {
        fetch("/accounts/create-checkout-session/")
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data);
            return stripe.redirectToCheckout()
        })
        .then((res) => {
            console.log(res);
        });
    });
});