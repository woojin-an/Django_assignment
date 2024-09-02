document.addEventListener('DOMContentLoaded', function() {
    const themeToggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    const containers = document.querySelectorAll('.container'); // 모든 컨테이너 선택

    // 현재 테마 상태를 로컬 저장소에서 가져옵니다.
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        body.classList.add('dark-theme');
        containers.forEach(container => container.classList.add('dark-theme'));
    }

    themeToggleButton.addEventListener('click', function() {
        const isDarkMode = body.classList.toggle('dark-theme');
        // 모든 컨테이너에 다크 테마 클래스를 적용합니다.
        containers.forEach(container => container.classList.toggle('dark-theme', isDarkMode));
        // 테마 상태를 로컬 저장소에 저장합니다.
        localStorage.setItem('darkMode', isDarkMode);
    });
});
