// Global variables
let allSongs = [];
let currentPage = 1;
const songsPerPage = 12;
let filteredSongs = [];
let currentType = 'top100';
let currentCategory = 'vietnam';
let currentSubcategory = 'nhactre';
let currentPlaylistId = '';

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Show welcome section and hide main content
    document.getElementById('welcomeSection').style.display = 'block';
    document.getElementById('mainContent').style.display = 'none';

    // Event listeners
    document.getElementById('scrapeBtn').addEventListener('click', triggerScraping);
    document.getElementById('searchBtn').addEventListener('click', searchSongs);
    document.getElementById('searchInput').addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            searchSongs();
        }
    });
    document.getElementById('exportCSVBtn').addEventListener('click', exportCSV);

    // Toggle sidebar
    document.getElementById('sidebarCollapse').addEventListener('click', function() {
        document.getElementById('sidebar').classList.toggle('active');
        document.getElementById('content').classList.toggle('active');
    });

    // Set up menu click handlers
    setupMenuHandlers();
});

// Setup menu click handlers
function setupMenuHandlers() {
    // Toggle submenu expansion
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const parent = this.parentElement;
            const submenu = this.nextElementSibling;

            // Determine menu level (level 1, 2 or 3)
            const level = getMenuLevel(parent);

            // Close sibling menus at the same level
            const allSameLevelItems = getAllSameLevelItems(parent, level);
            allSameLevelItems.forEach(item => {
                if (item !== parent) {
                    item.classList.remove('menu-open');
                    const sub = item.querySelector('.submenu');
                    if (sub) sub.style.display = 'none';

                    const icon = item.querySelector('.toggle-btn i');
                    if (icon) {
                        icon.classList.remove('bi-chevron-up');
                        icon.classList.add('bi-chevron-down');
                    }
                }
            });

            // Toggle menu hiện tại
            const isOpen = parent.classList.toggle('menu-open');
            if (submenu) {
                submenu.style.display = isOpen ? 'block' : 'none';
            }

            const icon = this.querySelector('.toggle-btn i');
            if (icon) {
                if (isOpen) {
                    icon.classList.remove('bi-chevron-down');
                    icon.classList.add('bi-chevron-up');
                } else {
                    icon.classList.remove('bi-chevron-up');
                    icon.classList.add('bi-chevron-down');
                }
            }
        });
    });

    // Set click handlers for content pages
    const menuItems = document.querySelectorAll('a[data-type]');
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();

            // Remove active class from all items
            menuItems.forEach(mi => mi.classList.remove('active'));

            // Add active class to clicked item
            this.classList.add('active');

            // Set current content type
            currentType = this.getAttribute('data-type');
            currentCategory = this.getAttribute('data-category');
            currentSubcategory = this.getAttribute('data-subcategory');

            // Show main content and hide welcome section
            document.getElementById('welcomeSection').style.display = 'none';
            document.getElementById('mainContent').style.display = 'block';

            // Update page title and description
            updatePageInfo();

            // Load songs for this selection
            loadSongsFromAPI();

            // On mobile, collapse sidebar
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('active');
                document.getElementById('content').classList.remove('active');
            }
        });
    });

    // Auto-expand active item's parents
    const activeItem = document.querySelector('a.active');
    if (activeItem) {
        let parent = activeItem.parentElement;
        while (parent && parent.id !== 'sidebar') {
            if (parent.classList.contains('submenu')) {
                parent.style.maxHeight = '1000px';
                parent.parentElement.classList.add('menu-open');
                const toggle = parent.parentElement.querySelector('.toggle-btn i');
                if (toggle) {
                    toggle.classList.remove('bi-chevron-down');
                    toggle.classList.add('bi-chevron-up');
                }
            }
            parent = parent.parentElement;
        }
    }

    // Hàm xác định cấp của menu
    function getMenuLevel(element) {
        let level = 0;
        let current = element;
        while (current && current.id !== 'sidebar') {
            if (current.classList.contains('submenu')) level++;
            current = current.parentElement;
        }
        return level + 1; // Level 1 ~ top-level in sidebar
    }

    // Hàm lấy tất cả li cùng cấp
    function getAllSameLevelItems(currentItem, level) {
        let parentList;
        if (level === 1) {
            parentList = document.querySelector('#sidebar > ul');
        } else {
            parentList = currentItem.parentElement; // ul.submenu
        }
        return parentList ? parentList.querySelectorAll(':scope > li') : [];
    }
}

// Update page title and description
function updatePageInfo() {
    const typeTitles = {
        'song': 'Bài Hát',
        'playlist': 'Playlist',
        'collection': 'Tuyển Tập',
        'top100': 'Top 100'
    };

    const categoryTitles = {
        'vietnam': 'Việt Nam',
        'usuk': 'Âu Mỹ',
        'asia': 'Châu Á',
        'other': 'Khác',
        'genre': 'Thể Loại',
        'mood': 'Tâm Trạng',
        'scene': 'Khung Cảnh',
        'topic': 'Chủ Đề'
    };

    const subcategoryTitles = {
        'nhactre': 'Nhạc Trẻ',
        'trutinh': 'Trữ Tình',
        'remixviet': 'Remix Việt',
        'rapviet': 'Rap Việt',
        'tienchien': 'Tiền Chiến',
        'nhactrinh': 'Nhạc Trịnh',
        'rockviet': 'Rock Việt',
        'cachmang': 'Cách Mạng',
        'pop': 'Pop',
        'rock': 'Rock',
        'electronicadance': 'Electronica/Dance',
        'rbhiphoprap': 'R&B/HipHop/Rap',
        'bluesjazz': 'Blues/Jazz',
        'country': 'Country',
        'latin': 'Latin',
        'indie': 'Indie',
        'aumy-khac': 'Âu Mỹ khác',
        'nhachan': 'Nhạc Hàn',
        'nhachoa': 'Nhạc Hoa',
        'nhacnhat': 'Nhạc Nhật',
        'nhacthai': 'Nhạc Thái',
        'thieunhi': 'Thiếu Nhi',
        'khongloi': 'Không Lời',
        'beat': 'Beat',
        'theloaikhac': 'Thể Loại Khác',
        'nhacphim': 'Nhạc Phim',
        'buon': 'Buồn',
        'hungphan': 'Hưng Phấn',
        'nhonhung': 'Nhớ Nhung',
        'thattinh': 'Thất Tình',
        'thugian': 'Thư Giãn',
        'vuive': 'Vui Vẻ',
        'cafe': 'Cafe',
        'barclub': 'Bar - Club',
        'phongtra': 'Phòng Trà',
        'tamboiloi': 'Tắm - Bơi Lội',
        'tapgym': 'Tập Gym',
        'langman': 'Lãng Mạn',
        'mua': 'Mưa',
        'tinhyeu': 'Tình Yêu',
        'top100': 'Top 100',
        'weekend': 'Weekend',
        'chillout': 'Chill Out',
        'bathu': 'Bất Hủ',
        'songca': 'Song Ca',
        'mashup': 'Mashup',
        'soundtrack': 'Soundtrack'
    };

    let pageTitle = '';
    let description = '';

    if (currentType === 'collection') {
        pageTitle = `${typeTitles[currentType]} ${subcategoryTitles[currentSubcategory]}`;
    } else {
        pageTitle = `${typeTitles[currentType]} ${subcategoryTitles[currentSubcategory]} ${categoryTitles[currentCategory]}`;
    }

    document.getElementById('pageTitle').textContent = pageTitle;

    if (currentType === 'top100') {
        description = `Danh sách Top 100 bài hát ${subcategoryTitles[currentSubcategory]} ${categoryTitles[currentCategory]} được yêu thích nhất.`;
    } else if (currentType === 'playlist') {
        description = `Danh sách các Playlist ${subcategoryTitles[currentSubcategory]} ${categoryTitles[currentCategory]} thịnh hành.`;
    } else if (currentType === 'collection') {
        if (['genre', 'mood', 'scene', 'topic'].includes(currentCategory)) {
            description = `Danh sách các Tuyển tập ${subcategoryTitles[currentSubcategory]}.`;
        } else {
            description = `Danh sách các Tuyển tập ${subcategoryTitles[currentSubcategory]} ${categoryTitles[currentCategory]}.`;
        }
    } else {
        description = `Danh sách các Bài hát ${subcategoryTitles[currentSubcategory]} ${categoryTitles[currentCategory]}.`;
    }

    document.getElementById('contentDescription').textContent = description;
}

// Load songs from API
function loadSongsFromAPI() {
    showStatus('info', 'Đang tải dữ liệu...');
    document.getElementById('songsList').innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-danger" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Đang tải dữ liệu...</p>
        </div>
    `;
    
    const apiUrl = `/api/songs?type=${currentType}&category=${currentCategory}&subcategory=${currentSubcategory}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(result => {
            if (result.data && result.data.length > 0) {
                allSongs = result.data;
                filteredSongs = [...allSongs];
                if (allSongs[0] && allSongs[0].date_scraped) {
                    document.getElementById('lastUpdate').textContent = formatDateTime(allSongs[0].date_scraped);
                }
                if (currentType === 'playlist' || currentType === 'collection') {
                    renderPlaylists();
                } else {
                    renderSongs(1);
                }
                showStatus('success', `Đã tải ${allSongs.length} mục thành công!`);
            } else {
                document.getElementById('songsList').innerHTML = `
                    <div class="col-12 text-center py-5">
                        <i class="bi bi-exclamation-triangle fs-1 text-warning"></i>
                        <p class="mt-2">Không tìm thấy dữ liệu. Vui lòng cào dữ liệu mới.</p>
                    </div>
                `;
                showStatus('warning', 'Không tìm thấy dữ liệu. Vui lòng cào dữ liệu mới.');
            }
        })
        .catch(error => {
            console.error('Error loading songs:', error);
            document.getElementById('songsList').innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-exclamation-circle fs-1 text-danger"></i>
                    <p class="mt-2">Lỗi khi tải dữ liệu: ${error.message || 'Không thể kết nối tới máy chủ'}</p>
                </div>
            `;
            showStatus('danger', 'Lỗi khi tải dữ liệu từ API.');
        });
}

// Render playlists with clickable items
function renderPlaylists() {
    let html = '';
    if (filteredSongs.length === 0) {
        html = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-search fs-1 text-muted"></i>
                <p class="mt-2">Không tìm thấy ${currentType === 'collection' ? 'tuyển tập' : 'playlist'} nào phù hợp với tìm kiếm của bạn.</p>
            </div>
        `;
    } else {
        filteredSongs.forEach(item => {
            html += `
                <div class="col-md-3">
                    <div class="card h-100 ${currentType}-card" data-playlist-id="${item.playlist_id}" data-playlist-url="${item.playlist_url}">
                        <img src="${item.img_url || 'https://stc-id.nixcdn.com/v11/images/img-plist-full.jpg'}" 
                            class="card-img-top" 
                            alt="${item.title}"
                            onerror="this.src='https://stc-id.nixcdn.com/v11/images/img-plist-full.jpg'">
                        <div class="card-body">
                            <h5 class="card-title song-title" title="${item.title}">${item.title}</h5>
                            <p class="card-text song-artist" title="${item.artists}">${item.artists}</p>
                            <p class="card-text">Số bài hát: ${item.song_count}</p>
                        </div>
                        <div class="card-footer bg-white border-0">
                            <button class="btn btn-sm btn-outline-danger w-100" onclick="${currentType === 'collection' ? 'loadCollectionSongs' : 'loadPlaylistSongs'}('${item.playlist_id}', '${item.title}')">
                                Xem bài hát
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
    }
    document.getElementById('songsList').innerHTML = html;
}

//load collection songs
function loadCollectionSongs(playlistId, collectionTitle) {
    showStatus('info', 'Đang tải danh sách bài hát...');
    document.getElementById('songsList').innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-danger" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Đang tải danh sách bài hát...</p>
        </div>
    `;
    
    // Update page title
    document.getElementById('pageTitle').textContent = `Danh sách bài hát: ${collectionTitle}`;
    document.getElementById('contentDescription').textContent = `Danh sách các bài hát trong tuyển tập ${collectionTitle}.`;
    
    // Store playlist ID for export
    currentPlaylistId = playlistId;
    currentType = 'collection_songs'; // Update type for export CSV

    fetch(`/api/collection-songs?playlist_id=${playlistId}&category=${currentCategory}&subcategory=${currentSubcategory}`)
        .then(response => response.json())
        .then(result => {
            if (result.data && result.data.length > 0) {
                allSongs = result.data;
                filteredSongs = [...allSongs];
                if (allSongs[0] && allSongs[0].date_scraped) {
                    document.getElementById('lastUpdate').textContent = formatDateTime(allSongs[0].date_scraped);
                }
                renderSongs(1);
                showStatus('success', `Đã tải ${allSongs.length} bài hát thành công!`);
            } else {
                document.getElementById('songsList').innerHTML = `
                    <div class="col-12 text-center py-5">
                        <i class="bi bi-exclamation-triangle fs-1 text-warning"></i>
                        <p class="mt-2">Không tìm thấy bài hát trong tuyển tập này. Vui lòng cào dữ liệu mới.</p>
                    </div>
                `;
                showStatus('warning', 'Không tìm thấy bài hát. Vui lòng cào dữ liệu mới.');
            }
        })
        .catch(error => {
            console.error('Error loading collection songs:', error);
            document.getElementById('songsList').innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-exclamation-circle fs-1 text-danger"></i>
                    <p class="mt-2">Lỗi khi tải dữ liệu: ${error.message || 'Không thể kết nối tới máy chủ'}</p>
                </div>
            `;
            showStatus('danger', 'Lỗi khi tải danh sách bài hát.');
        });
}

// Load songs from a specific playlist
function loadPlaylistSongs(playlistId, playlistTitle) {
    showStatus('info', 'Đang tải danh sách bài hát...');
    document.getElementById('songsList').innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-danger" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Đang tải danh sách bài hát...</p>
        </div>
    `;
    
    // Update page title
    document.getElementById('pageTitle').textContent = `Danh sách bài hát: ${playlistTitle}`;
    document.getElementById('contentDescription').textContent = `Danh sách các bài hát trong playlist ${playlistTitle}.`;
    
    // Store playlist ID for export
    currentPlaylistId = playlistId;

    fetch(`/api/playlist-songs?playlist_id=${playlistId}&category=${currentCategory}&subcategory=${currentSubcategory}`)
        .then(response => response.json())
        .then(result => {
            if (result.data && result.data.length > 0) {
                allSongs = result.data;
                filteredSongs = [...allSongs];
                if (allSongs[0] && allSongs[0].date_scraped) {
                    document.getElementById('lastUpdate').textContent = formatDateTime(allSongs[0].date_scraped);
                }
                renderSongs(1);
                showStatus('success', `Đã tải ${allSongs.length} bài hát thành công!`);
            } else {
                document.getElementById('songsList').innerHTML = `
                    <div class="col-12 text-center py-5">
                        <i class="bi bi-exclamation-triangle fs-1 text-warning"></i>
                        <p class="mt-2">Không tìm thấy bài hát trong playlist này. Vui lòng cào dữ liệu mới.</p>
                    </div>
                `;
                showStatus('warning', 'Không tìm thấy bài hát. Vui lòng cào dữ liệu mới.');
            }
        })
        .catch(error => {
            console.error('Error loading playlist songs:', error);
            document.getElementById('songsList').innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-exclamation-circle fs-1 text-danger"></i>
                    <p class="mt-2">Lỗi khi tải dữ liệu: ${error.message || 'Không thể kết nối tới máy chủ'}</p>
                </div>
            `;
            showStatus('danger', 'Lỗi khi tải danh sách bài hát.');
        });
}

// Render songs with pagination
function renderSongs(page) {
    currentPage = page;
    const start = (page - 1) * songsPerPage;
    const end = start + songsPerPage;
    const songsToRender = filteredSongs.slice(start, end);

    let html = '';

    if (songsToRender.length === 0) {
        html = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-search fs-1 text-muted"></i>
                <p class="mt-2">Không tìm thấy bài hát nào phù hợp với tìm kiếm của bạn.</p>
            </div>
        `;
    } else {
        songsToRender.forEach(song => {
            // Only show rank badge for top100 type and when rank is non-empty
            const rankBadge = currentType === 'top100' && song.rank && song.rank !== '' ? `
                <span class="badge ${song.rank <= 3 ? `rank-${song.rank}` : 'bg-dark'} rank-badge">#${song.rank}</span>
            ` : '';

            html += `
                <div class="col-md-3">
                    <div class="card h-100">
                        <span class="position-relative">
                            <img src="${song.img_url || 'https://stc-id.nixcdn.com/v11/images/avatar_default.jpg'}" 
                                class="card-img-top song-img" 
                                alt="${song.title}"
                                onerror="this.src='https://stc-id.nixcdn.com/v11/images/avatar_default.jpg'">
                            <i class="bi bi-soundwave soundwave-overlay position-absolute" style="display: none;top: 50%;left: 50%;transform: translate(-50%, -50%);font-size: 5rem;color: rgb(220 53 69);"></i>
                            ${rankBadge}
                        </span>
                        <div class="card-body">
                            <h5 class="card-title song-title" title="${song.title}">${song.title}</h5>
                            <p class="card-text song-artist" title="${song.artists}">${song.artists}</p>
                        </div>
                        <div class="card-footer bg-white border-0 song">
                            <button class="btn btn-sm btn-outline-danger w-100" data-song-url="${song.song_url}" onclick="playSong(this)">
                                <i class="bi bi-play-fill play-icon"></i>
                                <span class="button-text">Nghe bài hát</span>
                                <i class="bi bi-arrow-clockwise spinner-icon" style="display: none;"></i>
                            </button>
                            <audio class="player" controls style="display: none;">
                                <source class="source" type="audio/mpeg">
                            </audio>
                        </div>
                    </div>
                </div>
            `;
        });
    }

    document.getElementById('songsList').innerHTML = html;
    renderPagination();
}

// Render pagination
function renderPagination() {
    const totalPages = Math.ceil(filteredSongs.length / songsPerPage);
    let paginationHtml = '';

    paginationHtml += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="return changePage(${currentPage - 1})">
                <i class="bi bi-chevron-left"></i>
            </a>
        </li>
    `;

    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, startPage + 4);

    for (let i = startPage; i <= endPage; i++) {
        paginationHtml += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="return changePage(${i})">${i}</a>
            </li>
        `;
    }

    paginationHtml += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="return changePage(${currentPage + 1})">
                <i class="bi bi-chevron-right"></i>
            </a>
        </li>
    `;

    document.getElementById('pagination').innerHTML = paginationHtml;
}

// Change page
function changePage(page) {
    if (page < 1 || page > Math.ceil(filteredSongs.length / songsPerPage)) {
        return false;
    }

    renderSongs(page);
    window.scrollTo(0, 0);
    return false;
}

// Search songs
function searchSongs() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();

    if (searchTerm === '') {
        filteredSongs = [...allSongs];
    } else {
        filteredSongs = allSongs.filter(song => 
            song.title.toLowerCase().includes(searchTerm) || 
            song.artists.toLowerCase().includes(searchTerm)
        );
    }

    renderSongs(1);
}

// Trigger scraping through API
function triggerScraping() {
    const scrapeBtn = document.getElementById('scrapeBtn');
    scrapeBtn.disabled = true;
    scrapeBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Đang cào dữ liệu...';
    document.getElementById('songsList').classList.add('loading');
    showStatus('info', 'Đang cào dữ liệu từ NhacCuaTui...');

    fetch('/api/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: currentType,
            category: currentCategory,
            subcategory: currentSubcategory
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showStatus('success', 'Cào dữ liệu thành công!');
            if (currentType === 'playlist' && !currentPlaylistId) {
                loadSongsFromAPI();
            } else if (currentType === 'collection' && !currentPlaylistId) {
                loadSongsFromAPI();
            } else if (currentType === 'playlist_songs') {
                loadPlaylistSongs(currentPlaylistId, document.getElementById('pageTitle').textContent.replace('Danh sách bài hát: ', ''));
            } else if (currentType === 'collection_songs') {
                loadCollectionSongs(currentPlaylistId, document.getElementById('pageTitle').textContent.replace('Danh sách bài hát: ', ''));
            } else {
                loadSongsFromAPI();
            }
        } else {
            showStatus('danger', `Cào dữ liệu thất bại: ${result.message}`);
        }
    })
    .catch(error => {
        showStatus('danger', `Lỗi khi gọi API: ${error.message}`);
        console.error('Error:', error);
    })
    .finally(() => {
        scrapeBtn.disabled = false;
        scrapeBtn.innerHTML = '<i class="bi bi-cloud-download"></i> Cào dữ liệu mới';
        document.getElementById('songsList').classList.remove('loading');
    });
}

// Export CSV via API
function exportCSV() {
    if (currentType === 'playlist_songs' && currentPlaylistId) {
        window.location.href = `/api/export-csv?type=playlist_songs&category=${currentCategory}&subcategory=${currentSubcategory}&playlist_id=${currentPlaylistId}`;
    } else if (currentType === 'collection_songs' && currentPlaylistId) {
        window.location.href = `/api/export-csv?type=collection_songs&category=${currentCategory}&subcategory=${currentSubcategory}&playlist_id=${currentPlaylistId}`;
    } else {
        window.location.href = `/api/export-csv?type=${currentType}&category=${currentCategory}&subcategory=${currentSubcategory}`;
    }
}

// Show status alerts
function showStatus(type, message) {
    const statusAlert = document.getElementById('statusAlert');
    statusAlert.className = `alert alert-${type}`;
    statusAlert.innerHTML = message;
    statusAlert.classList.remove('d-none');

    setTimeout(() => {
        statusAlert.classList.add('d-none');
    }, 5000);
}

// Format date time
function formatDateTime(dateTimeStr) {
    try {
        const date = new Date(dateTimeStr);
        return date.toLocaleString('vi-VN');
    } catch (e) {
        return dateTimeStr;
    }
}

// Play song button
function playSong(button) {
    const songUrl = button.getAttribute('data-song-url');
    if (!songUrl) {
        console.error('Không tìm thấy song_url');
        return;
    }

    // Tìm các phần tử liên quan
    const audioElement = button.nextElementSibling;
    if (!audioElement || !audioElement.classList.contains('player')) {
        console.error('Không tìm thấy thẻ audio tương ứng');
        return;
    }

    const sourceElement = audioElement.querySelector('.source');
    if (!sourceElement) {
        console.error('Không tìm thấy thẻ source');
        return;
    }

    const playIcon = button.querySelector('.play-icon');
    const buttonText = button.querySelector('.button-text');
    const spinnerIcon = button.querySelector('.spinner-icon');
    const card = button.closest('.card');
    const soundwaveOverlay = card.querySelector('.soundwave-overlay');
    const songImg = card.querySelector('.song-img');

    // Nếu audio đang phát, tạm dừng và cập nhật UI
    if (!audioElement.paused) {
        audioElement.pause();
        playIcon.classList.remove('bi-soundwave');
        playIcon.classList.add('bi-play-fill');
        buttonText.textContent = 'Nghe bài hát';
        soundwaveOverlay.style.display = 'none';
        songImg.classList.remove('playing');
        return;
    }

    // Tạm dừng tất cả các audio khác và đặt lại UI
    const allAudioElements = document.querySelectorAll('audio');
    const allButtons = document.querySelectorAll('.btn[data-song-url]');
    allAudioElements.forEach(audio => {
        if (audio !== audioElement) {
            audio.pause();
            audio.currentTime = 0;
        }
    });
    allButtons.forEach(btn => {
        const icon = btn.querySelector('.play-icon');
        const text = btn.querySelector('.button-text');
        const spinner = btn.querySelector('.spinner-icon');
        const btnCard = btn.closest('.card');
        const overlay = btnCard.querySelector('.soundwave-overlay');
        const img = btnCard.querySelector('.song-img');
        icon.classList.remove('bi-soundwave');
        icon.classList.add('bi-play-fill');
        text.textContent = 'Nghe bài hát';
        spinner.style.display = 'none';
        overlay.style.display = 'none';
        img.classList.remove('playing');
    });

    // Hiển thị loading
    playIcon.style.display = 'none';
    buttonText.textContent = 'Đang tải';
    spinnerIcon.style.display = 'inline-block';

    // Gọi API /api/get-mp3
    fetch(`/api/get-mp3?song_url=${encodeURIComponent(songUrl)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.mp3_url) {
                // Cập nhật nguồn audio và phát
                sourceElement.src = `/proxy-mp3?mp3_url=${encodeURIComponent(data.mp3_url)}`;
                audioElement.load();
                audioElement.play().then(() => {
                    // Cập nhật UI khi phát
                    playIcon.style.display = 'inline-block';
                    playIcon.classList.remove('bi-play-fill');
                    playIcon.classList.add('bi-soundwave');
                    buttonText.textContent = 'Tạm dừng';
                    spinnerIcon.style.display = 'none';
                    soundwaveOverlay.style.display = 'block';
                    songImg.classList.add('playing');
                }).catch(err => {
                    // Xử lý lỗi phát
                    playIcon.style.display = 'inline-block';
                    playIcon.classList.remove('bi-soundwave');
                    playIcon.classList.add('bi-play-fill');
                    buttonText.textContent = 'Nghe bài hát';
                    spinnerIcon.style.display = 'none';
                    console.error('Lỗi phát audio:', err);
                    alert('Lỗi phát audio: ' + err.message);
                });
            } else {
                // Xử lý lỗi API
                playIcon.style.display = 'inline-block';
                playIcon.classList.remove('bi-soundwave');
                playIcon.classList.add('bi-play-fill');
                buttonText.textContent = 'Nghe bài hát';
                spinnerIcon.style.display = 'none';
                console.error('Lỗi từ API:', data.error);
                alert('Không thể lấy link MP3: ' + data.error);
            }
        })
        .catch(error => {
            // Xử lý lỗi mạng
            playIcon.style.display = 'inline-block';
            playIcon.classList.remove('bi-soundwave');
            playIcon.classList.add('bi-play-fill');
            buttonText.textContent = 'Nghe bài hát';
            spinnerIcon.style.display = 'none';
            console.error('Lỗi khi gọi API:', error);
            alert('Lỗi: ' + error.message);
        });
}