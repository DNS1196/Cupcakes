const BASE_URL = 'http://127.0.0.1:5000/api'


function generateCupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
}

async function showCupcakeList() {
    const resp = await axios.get(`${BASE_URL}/cupcakes`)
    console.log(resp)
    for (let cupcake of resp.data.cupcakes) {

        let newCC = generateCupcakeHTML(cupcake);
        $('.cupcake-list').append(newCC)
    }
}

$('.new-cupcake').on("submit", async function (e) {
    e.preventDefault();

    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

    const newCC = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, size, rating, image
    });
    console.log(newCC)
    $(".cupcake-list").empty()
    showCupcakeList()
    $('.new-cupcake').trigger("reset");

});

$(".cupcake-list").on("click", ".delete-button", async function (e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    console.log(cupcakeId)

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showCupcakeList())