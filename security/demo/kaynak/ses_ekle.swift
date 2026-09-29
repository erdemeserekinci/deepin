// Videoya ses izi ekler (macOS, AVFoundation): swift kaynak/ses_ekle.swift <video.mp4> <ses.m4a> <cikti.mp4>
// Video yeniden kodlanmaz (passthrough). ffmpeg olmayan makinede ses_yap.py bunu kullanir.
import AVFoundation
import Foundation

let arg = CommandLine.arguments
guard arg.count == 4 else {
    FileHandle.standardError.write("kullanim: swift ses_ekle.swift <video.mp4> <ses.m4a> <cikti.mp4>\n".data(using: .utf8)!)
    exit(2)
}
let videoURL = URL(fileURLWithPath: arg[1])
let sesURL = URL(fileURLWithPath: arg[2])
let ciktiURL = URL(fileURLWithPath: arg[3])
try? FileManager.default.removeItem(at: ciktiURL)

let video = AVURLAsset(url: videoURL)
let ses = AVURLAsset(url: sesURL)
let bileske = AVMutableComposition()

do {
    let sure = try await video.load(.duration)
    guard let vIz = try await video.loadTracks(withMediaType: .video).first else { throw NSError(domain: "ses_ekle", code: 1, userInfo: [NSLocalizedDescriptionKey: "videoda goruntu izi yok"]) }
    guard let sIz = try await ses.loadTracks(withMediaType: .audio).first else { throw NSError(domain: "ses_ekle", code: 2, userInfo: [NSLocalizedDescriptionKey: "ses dosyasinda ses izi yok"]) }
    let sesSure = try await ses.load(.duration)
    let aralik = CMTimeRange(start: .zero, duration: sure)
    let vYeni = bileske.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
    try vYeni.insertTimeRange(aralik, of: vIz, at: .zero)
    vYeni.preferredTransform = try await vIz.load(.preferredTransform)
    let sYeni = bileske.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
    try sYeni.insertTimeRange(CMTimeRange(start: .zero, duration: CMTimeMinimum(sure, sesSure)), of: sIz, at: .zero)
    guard let disa = AVAssetExportSession(asset: bileske, presetName: AVAssetExportPresetPassthrough) else {
        throw NSError(domain: "ses_ekle", code: 3, userInfo: [NSLocalizedDescriptionKey: "disa aktarma baslatilamadi"])
    }
    disa.outputURL = ciktiURL
    disa.outputFileType = .mp4
    disa.shouldOptimizeForNetworkUse = true
    await disa.export()
    if disa.status != .completed {
        throw disa.error ?? NSError(domain: "ses_ekle", code: 4, userInfo: [NSLocalizedDescriptionKey: "disa aktarma bitmedi"])
    }
    print("yazildi:", ciktiURL.path)
} catch {
    FileHandle.standardError.write("HATA: \(error.localizedDescription)\n".data(using: .utf8)!)
    exit(1)
}
