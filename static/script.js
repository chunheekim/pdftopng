document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const downloadSection = document.getElementById('download-section');
    const downloadLinks = document.getElementById('download-links');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // 폼 기본 동작 막기

        const formData = new FormData(form);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('서버 오류');
            }

            const data = await response.json();

            // 기존 링크 지우기
            downloadLinks.innerHTML = '';

            if (data.png_urls && data.png_urls.length > 0) {
                data.png_urls.forEach((url, index) => {
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `page_${index + 1}.png`;
                    link.textContent = `페이지 ${index + 1} 다운로드`;
                    link.style.display = 'block';
                    downloadLinks.appendChild(link);
                });
                downloadSection.style.display = 'block';
            } else {
                alert('변환된 이미지가 없습니다.');
            }

        } catch (err) {
            alert('업로드 중 오류가 발생했습니다: ' + err.message);
        }
    });
});
