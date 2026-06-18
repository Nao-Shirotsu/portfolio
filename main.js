/* =================================================================
   作品グリッドの動画再生制御（このファイルの責務はこれだけ）

   - 画面内に入った <video> を play()、画面外に出たら pause()
     → 作品数が増えてもモバイルが破綻しないための必須処理
   - prefers-reduced-motion: reduce のユーザーには自動再生せず
     poster 画像のみを見せる
   - IntersectionObserver / matchMedia 非対応環境では
     HTML 側の autoplay 属性にそのまま委ねる（グレースフルデグレード）
   ================================================================= */
(function () {
  "use strict";

  var videos = Array.prototype.slice.call(
    document.querySelectorAll("video.work__media")
  );
  if (videos.length === 0) return;

  var reduceMotionMQ =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  /* 再生は失敗し得る（自動再生ポリシー等）ので必ず握りつぶす */
  function safePlay(video) {
    var p = video.play();
    if (p && typeof p.catch === "function") p.catch(function () {});
  }

  /* reduced-motion 時：自動再生を止め、poster を再表示する */
  function freezeToPoster(video) {
    video.removeAttribute("autoplay");
    video.pause();
    // load() でメディアを初期状態へ戻し、確実に poster を見せる
    try { video.load(); } catch (e) {}
  }

  var observer = null;

  function startObserving() {
    if (!("IntersectionObserver" in window)) return; // 非対応は autoplay 任せ

    observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var video = entry.target;
          if (entry.isIntersecting) {
            safePlay(video);
          } else {
            video.pause();
          }
        });
      },
      { threshold: 0.1 }
    );

    videos.forEach(function (video) {
      video.pause(); // 初期状態は停止。可視判定で必要な分だけ再生
      observer.observe(video);
    });
  }

  function stopObserving() {
    if (!observer) return;
    videos.forEach(function (video) {
      observer.unobserve(video);
    });
    observer.disconnect();
    observer = null;
  }

  /* 現在の設定に応じて挙動を切り替え（設定変更にも追従） */
  function apply() {
    var reduce = reduceMotionMQ && reduceMotionMQ.matches;
    if (reduce) {
      stopObserving();
      videos.forEach(freezeToPoster);
    } else {
      startObserving();
    }
  }

  apply();

  /* OS の「視差効果を減らす」設定が切り替わったら追従 */
  if (reduceMotionMQ) {
    var onChange = function () { apply(); };
    if (reduceMotionMQ.addEventListener) {
      reduceMotionMQ.addEventListener("change", onChange);
    } else if (reduceMotionMQ.addListener) {
      reduceMotionMQ.addListener(onChange); // 旧Safari互換
    }
  }
})();
