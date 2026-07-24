import { useRef, useEffect, useState, useCallback } from 'react'
import type { IPCFrameEvent } from '../../types'
import { phoneBot } from '../../api'

interface Props {
  serial: string
}

export function ScreenCanvas({ serial }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [frame, setFrame] = useState<IPCFrameEvent | null>(null)
  const [coords, setCoords] = useState<{ x: number; y: number } | null>(null)
  const [phoneCoords, setPhoneCoords] = useState<{ x: number; y: number } | null>(null)
  const imageRef = useRef<HTMLImageElement | null>(null)

  useEffect(() => {
    const unsubscribe = phoneBot.onFrame((newFrame: IPCFrameEvent) => {
      setFrame(newFrame)
    })

    phoneBot.takeScreenshot(serial).then((screenshot) => {
      setFrame(screenshot)
    })

    return unsubscribe
  }, [serial])

  // Draw frame on canvas
  useEffect(() => {
    if (!frame || !canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const img = new Image()
    img.onload = () => {
      imageRef.current = img
      canvas.width = img.naturalWidth
      canvas.height = img.naturalHeight
      ctx.drawImage(img, 0, 0)
    }
    img.src = frame.data
  }, [frame])

  const getPhoneCoordinates = useCallback(
    (clientX: number, clientY: number) => {
      const canvas = canvasRef.current
      const img = imageRef.current
      if (!canvas || !img) return null

      const rect = canvas.getBoundingClientRect()
      const scaleX = img.naturalWidth / rect.width
      const scaleY = img.naturalHeight / rect.height

      return {
        x: Math.round((clientX - rect.left) * scaleX),
        y: Math.round((clientY - rect.top) * scaleY)
      }
    },
    []
  )

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      const phone = getPhoneCoordinates(e.clientX, e.clientY)
      setCoords({ x: e.clientX, y: e.clientY })
      setPhoneCoords(phone)
    },
    [getPhoneCoordinates]
  )

  const handleClick = useCallback(
    async (e: React.MouseEvent) => {
      const phone = getPhoneCoordinates(e.clientX, e.clientY)
      if (!phone) return

      await phoneBot.sendCommand({
        serial,
        action: 'tap',
        x: phone.x,
        y: phone.y,
        xRandom: 2,
        yRandom: 2
      })

      // Flash effect
      const canvas = canvasRef.current
      if (canvas) {
        const ctx = canvas.getContext('2d')
        if (ctx && imageRef.current) {
          const rect = canvas.getBoundingClientRect()
          const x = e.clientX - rect.left
          const y = e.clientY - rect.top

          ctx.save()
          ctx.beginPath()
          ctx.arc(x, y, 15, 0, Math.PI * 2)
          ctx.fillStyle = 'rgba(34, 197, 94, 0.4)'
          ctx.fill()
          ctx.restore()

          setTimeout(() => {
            if (imageRef.current) {
              ctx.clearRect(0, 0, canvas.width, canvas.height)
              ctx.drawImage(imageRef.current, 0, 0)
            }
          }, 150)
        }
      }
    },
    [serial, getPhoneCoordinates]
  )

  const handleMouseLeave = () => {
    setCoords(null)
    setPhoneCoords(null)
  }

  return (
    <div
      ref={containerRef}
      className="screen-canvas-container"
      onMouseMove={handleMouseMove}
      onClick={handleClick}
      onMouseLeave={handleMouseLeave}
    >
      <canvas
        ref={canvasRef}
        className="screen-canvas"
      />
      {phoneCoords && (
        <div className="coordinate-display">
          📍 ({phoneCoords.x}, {phoneCoords.y})
        </div>
      )}
    </div>
  )
}
