document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("inventory-body");
  const searchInput = document.getElementById("search");
  const searchBtn = document.getElementById("search-btn");

  let inventory = [];

  async function fetchInventory() {
    try {
      const response = await fetch("/api/inventory");
      if (!response.ok) {
        console.error("Failed to fetch inventory:", response.status, response.statusText);
        tableBody.innerHTML = `<tr><td colspan="6" style="color: red;">Failed to load inventory data.</td></tr>`;
        return;
      }
      inventory = await response.json();
      console.log("Fetched inventory count:", inventory.length);
      renderTable(inventory);
    } catch (error) {
      console.error("Error fetching inventory:", error);
      tableBody.innerHTML = `<tr><td colspan="6" style="color: red;">Error loading inventory data.</td></tr>`;
    }
  }

  function renderTable(data) {
    console.log("Rendering rows:", data.length);
    tableBody.innerHTML = "";
    if (data.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center text-danger">No results found.</td>
        </tr>
      `;
      return;
    }

    data.forEach(item => {
      const row = document.createElement("tr");

      if (item.low_stock) {
        row.classList.add("low-stock");
      }

      row.innerHTML = `
        <td>${item.sku}</td>
        <td>${item.item_name}</td>
        <td>${item.item_type}</td>
        <td>${item.quantity}</td>
        <td>${item.reorder_threshold}</td>
        <td>${item.expiration_date || "-"}</td>
      `;

      tableBody.appendChild(row);
    });
  }

  function handleSearch() {
    const term = searchInput.value.trim().toLowerCase();
    console.log("Search term:", term);

    if (!term) {
      renderTable(inventory);
      return;
    }

    const filtered = inventory.filter(item =>
      item.sku.toLowerCase().includes(term) ||
      item.item_name.toLowerCase().includes(term)
    );

    console.log("Filtered results count:", filtered.length);
    renderTable(filtered);
  }

  searchBtn.addEventListener("click", handleSearch);

  searchInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      handleSearch();
    }
  });

  fetchInventory();
});
