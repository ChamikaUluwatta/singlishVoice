import type { DetailedHTMLProps, HTMLAttributes } from 'react'

declare module 'react' {
  namespace JSX {
    type MaterialElementProps = DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement> & {
      [attr: string]: unknown
      disabled?: boolean
      value?: string
      selected?: boolean
      checked?: boolean
    }

    interface IntrinsicElements {
      [tagName: `md-${string}`]: MaterialElementProps
    }
  }
}

export {}
